import os
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from flasgger import Swagger

from security import authenticate, identity

API_VERSION = 'v1'
API_PATH = '/api/{}'.format(API_VERSION)

app = Flask(__name__)
app.secret_key = "PALO"
api = Api(app)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
swagger = Swagger(app)

jwt = JWT(app, authenticate, identity)

items = []


class Item(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        name = parser.parse_args().get('name')
        if name:
            item = next(filter(lambda x: x['name'] == name, items), None)
            return {'item': item}, 200 if item is not None else 404
        else:
            return {'message': "malformed body"}, 400

    @jwt_required()
    def post(self):
        request_data = request.get_json(force=True)
        name = request_data['name']
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {"message": "{} already exists".format(name)}, 400
        item = {
            'id': len(items) + 1,
            'name': name,
            'price': request_data['price']
        }
        items.append(item)
        return item, 201

    @jwt_required()
    def delete(self):
        global items
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        name = parser.parse_args().get('name')
        items = list(filter(lambda x: x['name'] != name, items))
        return {'items': items}

    def put(self):
        request_data = request.get_json()
        name = request_data['name']
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {
                'id': len(items) + 1,
                'name': name,
                'price': request_data['price']
            }
            items.append(item)
        else:
            item.update(request_data)
        return item


class ItemID(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True)
        _id = parser.parse_args().get('id')
        if _id:
            item = next(filter(lambda x: x['id'] == _id, items), None)
            return {'item': item}, 200 if item is not None else 404
        else:
            return {"message":'malformed request body'}, 400


class ItemList(Resource):

    def get(self):
        return {'items': items}


api.add_resource(Item, '{}/item'.format(API_PATH))
api.add_resource(ItemList, '{}/items'.format(API_PATH))
api.add_resource(ItemID, '{}/item_id'.format(API_PATH))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)



