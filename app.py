from flask_restful import Api
from resources import KijijiAds

from db import app
api = Api(app)

api.add_resource(KijijiAds, '/car-api/make=<string:make>&model=<string:model>')
