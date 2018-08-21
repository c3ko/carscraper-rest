from db import db
from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, asc, desc
from sqlalchemy.orm import relationship
class CarAd(db.Model):
    __table__  = db.Model.metadata.tables['car_ad']

    def __repr__(self):
        return self.full_name

if __name__ == '__main__':
    query = db.session.query(CarAd).filter_by(make = 'Toyota', model = 'Sienna').order_by(desc(CarAd.mileage))
    paginated_query = query.paginate(page=1, per_page=50, error_out=False)
    for item in paginated_query.items:
        print(item.mileage)

class SavedSearches(db.Model):
    __table__ = db.Model.metadata['saved_searches']
    id = Column(Integer, primary_key=True)
    saved_car_rel = relationship('SavedCar', back_populates='save_id')
    name = Column(String)
    date = Column(DateTime)
    num_saved = Column(Integer)

    def __repr__(self):
        return 'SavedSearch: ' + self.name

class SavedCar(db.Model):
    __table__ = db.Model.metadata['saved_cars']
    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, ForeignKey('car_ad.id'))
    car_rel = relationship('CarAd', back_populates='saved_car_rel')
    save_id = Column(Integer, ForeignKey('saved_searches.id'))
    save_search_rel = relationship('SavedSearches', back_populates='saved_car_rel')


