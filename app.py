from flask_restful import Api
from resources import KijijiAds

from db import app
api = Api(app)

api.add_resource(KijijiAds, '/<string:make>')
if __name__ == '__main__':
    app.run()