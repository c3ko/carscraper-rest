from flask import request, jsonify
from flask_restful import Resource
from sqlalchemy import desc, asc, distinct
from db import db
from models import CarAd, SavedSearch, SavedCar
from datetime import datetime
import json

carAd_cols = {
    'make': CarAd.make,
    'model': CarAd.model,
    'year': CarAd.year,
    'mileage': CarAd.mileage,
    'location': CarAd.location,
    'price': CarAd.price,
    'date_posted': CarAd.date_posted
}

def all_columns(row):
    result = {}
    col_keys = row.__table__.columns.keys()

    for col in col_keys:
        result[col] = getattr(row, col)
    return result

class Kijijiad(Resource):
    def get(self, car_id):
        pass

class KijijiAdSearch(Resource):
    def get(self, make='', model='', page='1', order='make', order_type='ASC'):
        
        item_list = {}

        col_order = carAd_cols[order]
        if order_type == 'DESC':
            col_order = desc(col_order)
        elif order_type == 'ASC':
            col_order = asc(col_order)

        query = db.session.query(CarAd).filter_by(make = make, model= model).order_by(col_order)
        paginated_query = query.paginate(page=page, per_page=15, error_out=False)
        item_list['pages'] = paginated_query.pages
        item_list['page'] = paginated_query.page
        item_list['total'] = paginated_query.total
        item_list['list'] = []
        for item in paginated_query.items:
            item_list['list'].append({'id': item.id, 'make': item.make, 'model': item.model, 'year': item.year, 'transmission': item.transmission,
             'mileage': item.mileage, 'price': item.price, 'location': item.location, 'full_name': item.full_name, 'description': item.description, 
             'date_posted': item.date_posted,'link': item.link})
        return jsonify(item_list)

class SavedSearchesList(Resource):
    def get(self):
        item_list = {}
        #fetch all save searches for menu
        query = db.session.query(SavedSearch).all()
        item_list['list'] = []
        for item in query:
            item_list['list'].append({'id' : item.id, 'name' : item.name, 'date_created' : item.date, 'num_saved' : item.num_saved})
        return jsonify (item_list)
    
    def post(self):
        name = request.form['name']
        saved_search = SavedSearch(name=name, date=datetime.now(), num_saved=0)
        db.session.add(saved_search)
        db.session.commit()

        return self.get()
        
class SavedSearches(Resource):


    def get(self, save_id):
        item_list = {}
        query = db.session.query(SavedSearch).filter_by(id=save_id)
        
        item_list['list'] = []
        for item in query:
            item_list['list'].append({'id' : item.id, 'name' : item.name, 'date_created' : item.date, 'num_saved' : item.num_saved})
        return jsonify (item_list)


    def post(self):
        item_list = {}
        name = request.form['name']
        saved_search = SavedSearch(name=name, date=datetime.now(), num_saved=0)
        db.session.add(saved_search)
        db.session.commit()
        query = db.session.query(SavedSearch).all()

        item_list['list'] = []
        for item in query:
            item_list['list'].append(all_columns(item))
        return jsonify (item_list)


    def delete(self, save_id):
        item_list = {}
        query = db.session.query(SavedSearch)
        save_to_be_deleted= query.filter_by(id=save_id).first()
        db.session.delete(save_to_be_deleted)
        db.session.commit()

        
        item_list['list'] = []
        for item in query.all():
            item_list['list'].append(all_columns(item))
        return jsonify (item_list)

class SavedCarsList(Resource):

    def post(self):
        item_list = {}
        save_id, car_id = request.form['save_id'], request.form['car_id']        
        saved_car = SavedCar(save_id=save_id,car_id=car_id)
        db.session.add(saved_car)

        #update count of number of cars in save
        num_car_saves = db.session.query(SavedCar).filter_by(id=save_id).count()
        db.session.query(SavedSearch).filter_by(id=save_id).update({"num_saved" : num_car_saves + 1})
        
        db.session.commit()

        query = db.session.query(SavedCar).all()
        item_list['list'] = []
        for item in query:
            item_list['list'].append(all_columns(item))
        return jsonify (item_list)


class SavedCars(Resource):
    # Get all saved cars for a particular save in paginated request

    def get(self, save_id):
        item_list = {}
        query = db.session.query(CarAd).join(CarAd.saved_car_rel).filter(SavedCar.save_id == save_id)
        item_list['save_id'] = save_id
        item_list['list'] = []
        for item in query:
            item_list['list'].append(all_columns(item))
        return jsonify (item_list)


    def delete(self, save_id):
        item_list = {}
        car_id = request.form['car_id']
        saved_car = db.session.query(SavedCar).filter_by(save_id=save_id, car_id=car_id).first()
        db.session.delete(saved_car)
        db.session.commit()

        query = db.session.query(CarAd).join(CarAd.saved_car_rel).all()
        item_list['list'] = []
        for item in query:
            item_list['list'].append(all_columns(item))
        return jsonify (item_list)