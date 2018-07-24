from flask import request, jsonify
from flask_restful import Resource
from db import db
from models import CarAd
import json
class KijijiAds(Resource):
    def get(self, make, model):
        
        item_list = {}
        
        for item in db.session.query(CarAd).filter_by(make = make, model= model):
            item_list[item.id] = {'id': item.id, 'make': item.make, 'model': item.model, 'year': item.year, 'transmission': item.transmission,
             'mileage': item.mileage, 'price': item.price, 'location': item.location, 'full_name': item.full_name, 'description': item.description, 
             'date_posted': item.date_posted,'link': item.link }
        return jsonify(item_list)
