from db import db
from sqlalchemy import asc, desc
class CarAd(db.Model):
    __table__  = db.Model.metadata.tables['car_ad']

    def __repr__(self):
        return self.full_name

if __name__ == '__main__':
    query = db.session.query(CarAd).filter_by(make = 'Toyota', model = 'Sienna').order_by(desc(CarAd.mileage))
    paginated_query = query.paginate(page=1, per_page=50, error_out=False)
    for item in paginated_query.items:
        print(item.mileage)