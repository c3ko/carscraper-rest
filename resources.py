from flask import request, jsonify
from flask_restful import Resource
from sqlalchemy import desc
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
    def get(self, make, model, page, order):
        
        item_list = {}
        

        query = db.session.query(CarAd).filter_by(make = make, model= model).paginate(page=page, 
        per_page=15, error_out=False).order_by(desc(carAd_cols[order]))

        for item in query.items:
            item_list[item.id] = {'id': item.id, 'make': item.make, 'model': item.model, 'year': item.year, 'transmission': item.transmission,
             'mileage': item.mileage, 'price': item.price, 'location': item.location, 'full_name': item.full_name, 'description': item.description, 
             'date_posted': item.date_posted,'link': item.link }
        return jsonify(item_list)

