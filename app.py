from flask_restful import Api

from resources import KijijiAds

from db import app
api = Api(app)

api.add_resource(KijijiAds, '/car-api/make=<string:make>&model=<string:model>')

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  return response