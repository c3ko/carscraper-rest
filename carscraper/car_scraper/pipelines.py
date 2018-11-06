# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import sqlite3
import logging
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.pool import NullPool

from scrapy import signals
from scrapy.utils.project import get_project_settings

from sqlalchemy import ForeignKey, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

DeclarativeBase = declarative_base()


class CarAd(DeclarativeBase):
    __tablename__ = 'car_ad'
    id = Column(Integer, primary_key=True)
    saved_car_rel = relationship('SavedCar', back_populates='car_rel')
    make = Column(String(50))
    model = Column(String(50))
    year = Column(Integer)
    transmission = Column(String(50))
    price = Column(Integer)
    mileage = Column(Integer)
    location = Column(String(500))
    full_name = Column(String(1000))
    description = Column(String(1000))
    date_posted = Column(DateTime)
    link = Column(String(500))


    def __init__(self, id=None, make=None, model=None, year=None, transmission=None, price=None, mileage=None, location=None,
    full_name=None, description=None, date_posted=None, link=None):
        self.id = id
        self.make = make
        self.model = model
        self.year = year
        self.transmission = transmission
        self.price = price
        self.mileage = mileage
        self.location = location
        self.full_name = full_name
        self.description = description
        self.date_posted = datetime.strptime(date_posted, "%Y-%m-%dT%H:%M:%S")
        self.link = link
    
    def __repr__(self):
        return (f'{self.full_name}')
    

class SavedCar(DeclarativeBase):
    __tablename__ = 'saved_cars'
    #__table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, ForeignKey('car_ad.id'))
    car_rel = relationship('CarAd', back_populates='saved_car_rel')
    save_id = Column(Integer, ForeignKey('saved_searches.id'))
    save_search_rel = relationship('SavedSearch', back_populates='saved_car_rel')

log = logging.getLogger(__name__)

class SavedSearch(DeclarativeBase):
    __tablename__ = 'saved_searches'
    #__table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True)
    saved_car_rel = relationship('SavedCar', back_populates='save_search_rel')
    name = Column(String)
    date = Column(DateTime)
    num_saved = Column(Integer)

    def __repr__(self):
        return 'SavedSearch: ' + self.name

'''
class KijijiPipeline(object):

    def __init__(self):
        self.conn = None
        self.cur = None
        self.setup_db()
        self.create_table()

    def setup_db(self):
        self.conn = sqlite3.connect('./car_scraper.db')
        self.cur = self.conn.cursor()

    def close_db(self):
        self.conn.close()

    def __del__(self):
        self.close_db()

    def create_table(self):
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS Kijiji(
            make TEXT,
            model TEXT,
            year INTEGER,
            full_name TEXT,
            price INTEGER,
            location TEXT,
            mileage INTEGER,
            date_posted DateTime,
            link TEXT,
            PRIMARY KEY (link, date_posted)
            )
            """
        )

    def insert_into_db(self, item):

        self.cur.execute(
            """
            INSERT INTO Kijiji VALUES ("{}","{}","{}","{}","{}","{}","{}",datetime("{}"),"{}")
            """.format(item['make'], item['model'], item['year'], str(item['full_name']), item['price'],
                       str(item['location']), str(item['mileage']), item['date_posted'], str(item['link']))
        )
        self.conn.commit()

    def process_item(self, item, spider):
        try:
            self.insert_into_db(item)

        except sqlite3.IntegrityError:
            pass
'''


class SQLAlchemyPipeline(object):
    def __init__(self, settings):
        self.DB = settings.get('DATABASE')
        self.sessions = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls(crawler.settings)
        crawler.signals.connect(pipeline.spider_on, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_off, signals.spider_closed)
        return pipeline

    def create_engine(self):
        db_engine = create_engine(URL(**self.DB), poolclass=NullPool)
        return db_engine
    

    def spider_on(self, spider):
        """
            When signalled from spider, creates engines, sessions and tables (if not already existing).
        """
        engine = self.create_engine()
        # checkfirst ensures that tables are created if they don't exist
        DeclarativeBase.metadata.create_all(engine, checkfirst=True)
        session = sessionmaker(bind=engine)()
        self.sessions[spider] = session
    
    def spider_off(self, spider):
        """
            Closes a session when it's associated spiders signals that it is finished
        """
        session = self.sessions[spider]
        session.close()
    
    def process_item(self, item, spider):
        session = self.sessions[spider]
        car_ad = CarAd(**item)

        # check if url has there is car ad with same URL in table
        ad_exists = session.query(CarAd).filter_by(link=item['link']).first() is not None

        if ad_exists:
            log.info(f' Ad: {car_ad} already exists in the database')
            return item
        try:
            session.add(car_ad)
            session.commit()
            log.info(f' Ad : {car_ad} has been inserted in to the database')

        except:
            log.info(f' Ad : {car_ad} cannot be inserted in to the database')
            session.rollback()
        
        return item
