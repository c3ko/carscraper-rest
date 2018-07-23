from db import db

class CarAd(db.Model):
    __table__  = db.Model.metadata.tables['car_ad']

    def __repr__(self):
        return self.full_name

if __name__ == '__main__':
    for item in db.session.query(CarAd).filter_by(make = 'Toyota', model = 'Sienna'):
        print(item)