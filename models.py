from db import db
from sqlalchemy import Table, Column, Integer, ForeignKey, String, DateTime, asc, desc
from sqlalchemy.orm import relationship
from datetime import datetime
db.Model.metadata.reflect(db.engine)

class CarAd(db.Model):
    __tablename__  = 'car_ad'
    __table_args__ = {'extend_existing': True} 

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

    def __repr__(self):
        return self.full_name

class SavedSearch(db.Model):
    __tablename__ = 'saved_searches'
    __table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True)
    saved_car_rel = relationship('SavedCar', back_populates='save_search_rel')
    name = Column(String)
    date = Column(DateTime)
    num_saved = Column(Integer)

    def __repr__(self):
        return 'SavedSearch: ' + self.name

class SavedCar(db.Model):
    __tablename__ = 'saved_cars'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, ForeignKey('car_ad.id'))
    car_rel = relationship('CarAd', back_populates='saved_car_rel')
    save_id = Column(Integer, ForeignKey('saved_searches.id'))
    save_search_rel = relationship('SavedSearch', back_populates='saved_car_rel')
    def __repr__(self):
        return 'SaveId: ' + self.save_id + ' CarId: ' + self.car_id
