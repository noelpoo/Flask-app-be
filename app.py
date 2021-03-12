import os
import time
import firebase_admin
import uuid
from firebase_admin import credentials
from firebase_admin import firestore
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS, cross_origin
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required

from security import *

project_id = 'item-app-c5681'
FIREBASE_KEY_PATH = './firebase/item-app-d4e6f69fdfa1.json'


cred = credentials.Certificate(FIREBASE_KEY_PATH)
firebase_admin.initialize_app(cred)
db = firestore.client()

API_VERSION = 'v1'
API_PATH = '/api/{}'.format(API_VERSION)
app = Flask(__name__)
app.secret_key = "PALO"
api = Api(app)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"/*": {"origins": "*"}})
jwt = JWTManager(app)



class Item(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        name = parser.parse_args().get('name')
        # if name:
        #     item = next(filter(lambda x: x['name'] == name, items), None)
        #     return {'item': item}, 200 if item is not None else 404
        # else:
        #     return {'message': "malformed body"}, 400
        if name:
            docs = db.collection('items').where('name', '==', name).stream()
            resp_list = [doc.to_dict() for doc in docs]
            if len(resp_list) != 0:
                return {
                    'item': resp_list[0]
                }, 200
            else:
                return {
                    'message': 'item not found'
                }, 404
        else:
            return {
                'message': 'missing query parameter {name}'
            }, 400


    @jwt_required
    @cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
    def post(self):
        request_data = request.get_json(force=True)
        name = request_data['name']
        docs = db.collection('items').stream()
        _items = [doc.to_dict() for doc in docs]
        docs = db.collection('items').where('name', '==', name).stream()
        resp_list = [doc.to_dict() for doc in docs]
        if name:
            if not resp_list:
                item = {
                    'id': len(_items) + 1,
                    'name': name,
                    'price': request_data['price'],
                    'create_time': round(time.time())
                }
                db.collection('items').document(str(uuid.uuid4())).set(item)
                return item, 201
            else:
                return {
                    'message': 'item already exists'
                }, 400
        else:
            return {
                'message': 'malformed request body'
            }, 400

    @jwt_required
    @cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
    # TODO - fix deletion of document from firebase using item name
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        name = parser.parse_args().get('name')
        if name:
            docs = db.collection('items').where('name', '==', name).stream()
            resp_list = [doc.to_dict() for doc in docs]

            # print('resp_list', resp_list)
            # print('resp_len', len(resp_list))
            # if len(resp_list) != 0:
            #     db.collection('items').where('name', '==', name).delete()
            #     docs = db.collection('items').stream()
            #     _items = [doc.to_dict() for doc in docs]
            #     return {'items': _items}
            # else:
            #     return {
            #         'message': "item not found"
            #     }, 404
        else:
            return {
                'message': 'missing query parameters'
            }, 400



class ItemID(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True)
        _id = parser.parse_args().get('id')
        if _id:
            # item = next(filter(lambda x: x['id'] == _id, items), None)
            # return {'item': item}, 200 if item is not None else 404
            docs = db.collection('items').where('id', '==', _id).stream()
            resp_list = [doc.to_dict() for doc in docs]
            if len(resp_list) !=0:
                return {
                    'item': resp_list[0]
                }, 200
            else:
                return {
                    'message': 'item not found'
                }, 404
        else:
            return {"message":'malformed request body'}, 400


class ItemList(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('sort', type=int, required=False)
        _sort = int(parser.parse_args().get('sort'))
        docs = db.collection('items').stream()
        _items = [doc.to_dict() for doc in docs]
        if _sort or _sort == 0:
            # sort by create time desc
            if _sort == 0:
                copy = sorted(_items, key=lambda k: k['create_time'], reverse=True)
                print(copy)
                return {'items': copy}
            # sort by create time asc
            elif _sort == 1:
                copy = sorted(_items, key=lambda k: k['create_time'], reverse=False)
                print(copy)
                return {'items': copy}
            # sort by name asc
            elif _sort == 2:
                copy = sorted(_items, key=lambda k: k['name'], reverse=False)
                return {'items': copy}
            elif _sort == 3:
                copy = sorted(_items, key=lambda k: k['name'], reverse=True)
                return {'items': copy}
        else:
            return {'items': _items}


class UserLogin(Resource):

    def post(self):
        data = request.get_json(force=True)
        print(data)
        user = username_table.get(data['username'], None)
        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        return {
            'message': 'invalid credentials'
        }, 401


api.add_resource(Item, '{}/item'.format(API_PATH))
api.add_resource(ItemList, '{}/items'.format(API_PATH))
api.add_resource(ItemID, '{}/item_id'.format(API_PATH))
api.add_resource(UserLogin, '{}/login'.format(API_PATH))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)



