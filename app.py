from flask_restful import Api

from resources import KijijiAdSearch, SavedCars, SavedCarsList, SavedSearches, SavedSearchesList

from db import app, db
api = Api(app)

api.add_resource(KijijiAdSearch, '/new-search/make=<string:make>&model=<string:model>/page-<int:page>&orderBy=<string:order>&orderType=<string:order_type>')
api.add_resource(SavedSearchesList, '/saved-search/')
api.add_resource(SavedSearches, '/saved-search/<int:save_id>')
api.add_resource(SavedCarsList, '/saved-car/')
api.add_resource(SavedCars, '/saved-car/<int:save_id>/page-<int:page>&orderBy=<string:order_by>&orderType=<string:order_type>')

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  return response

if __name__ == '__main__':
  app.run(host='127.0.0.1', port='5000')

