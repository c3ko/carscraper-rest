from flask import request, jsonify
from flask_restful import Resource
from sqlalchemy import desc, asc, distinct
from db import db
from models import CarAd
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
class KijijiAds(Resource):
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


class SavedSearches(Resource):
    def get(self, name):
        pass
    def put(self, name, date):
        db.session.
