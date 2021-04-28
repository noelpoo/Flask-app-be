import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import request
from flask_restful import Resource, reqparse
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required

from common import *

if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_KEY_PATH)
    default_app = firebase_admin.initialize_app(cred)

db = firestore.client()


class Item:
    def __init__(self, _id, name, price, create_time):
        self.id = _id
        self.name = name
        self.price = price
        self.create_time = create_time

    @classmethod
    def find_all_items(cls):
        doc_ref = db.collection(ITEM_FB_DB).stream()
        docs = [doc.to_dict() for doc in doc_ref]
        if docs:
            return [
                cls(item['id'], item['name'],
                    item['price'], item['create_time'])
                for item in docs
            ]
        else:
            return None

    @classmethod
    def find_all_items_sorted(cls, sort_val):
        doc_ref = db.collection(ITEM_FB_DB).stream()
        docs = [doc.to_dict() for doc in doc_ref]
        if docs:
            return [
                cls(i['id'], i['name'],
                    i['price'], i['create_time'])
                for i in sorted(docs, key=lambda k: k[SORT_MAP.get(sort_val)['key']],
                                reverse=SORT_MAP.get(sort_val)['desc'])
            ]
        else:
            return None

    @classmethod
    def find_by_id(cls, _id):
        doc_ref = db.collection(ITEM_FB_DB).document(_id)
        doc = doc_ref.get()
        item = doc.to_dict()
        if item:
            return cls(item['id'], item['name'], item['price'], item['create_time'])
        else:
            return None

    @classmethod
    def find_by_name(cls, name):
        doc_ref = db.collection(ITEM_FB_DB).where('name', '==', name).stream()
        docs = [doc.to_dict() for doc in doc_ref]
        if docs:
            item = docs[0]
            return cls(item['id'], item['name'], item['price'], item['create_time'])
        else:
            return None

    @classmethod
    def check_if_item_exists(cls, data):
        exists = False
        if cls.find_all_items():
            for item in cls.find_all_items():
                if data['name'] == item.name:
                    exists = True
                    break
        return exists

    @classmethod
    def find_latest_id_value(cls):
        items = cls.find_all_items()
        if items:
            return max([item.id for item in items])
        else:
            return 0

    @staticmethod
    def add_item_to_db(obj):
        try:
            item = {
                'id': obj.id,
                'name': obj.name,
                'price': obj.price,
                'create_time': obj.create_time
            }
            print('obj id: {}'.format(obj.id))
            db.collection(ITEM_FB_DB).document(str(obj.id)).set(item)
            return item
        except ValueError:
            return None

    @staticmethod
    def delete_item_using_id(_id):
        db.collection(ITEM_FB_DB).document(str(_id)).delete()


class ItemResource(Resource):

    @cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str, required=False, help='id or name missing in query parameters')
        parser.add_argument('name', type=str, required=False, help='id or name missing in query parameters')
        _id = parser.parse_args().get('id')
        name = parser.parse_args().get('name')

        if _id and name:
            return {
                       'message': 'Expected 1 query parameter'
                   }, 403
        elif _id:
            result = Item.find_by_id(_id)
            if result:
                return {
                           'item': {
                               'id': result.id,
                               'name': result.name,
                               'price': result.price,
                               'create_time': result.create_time
                           }
                       }, 200
            else:
                return {
                           'message': 'item with id {} is not found'.format(_id)
                       }, 404

        elif name:
            result = Item.find_by_name(name)
            if result:
                return {
                           'item': {
                               'id': result.id,
                               'name': result.name,
                               'price': result.price,
                               'create_time': result.create_time
                           }
                       }, 200
            else:
                return {
                           'message': 'item with name {} is not found'.format(name)
                       }, 404

        else:
            return {
                       'message': 'Expected 1 query parameter'
                   }, 403

    @jwt_required
    @cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
    def post(self):
        data = request.get_json(force=True)

        if not Item.check_if_item_exists(data):
            try:
                item = Item(Item.find_latest_id_value() + 1, data['name'],
                            data['price'], round(time.time()))
                result = Item.add_item_to_db(item)
                if result:
                    return {
                               'item': result
                           }, 201
                else:
                    return {
                               'message': "something went wrong"
                           }, 400
            except ValueError:
                return {
                           'message': "request body is malformed"
                       }, 400
        else:
            return {
                       'message': 'item with name: {} already exists'.format(data['name'])
                   }, 403

    @jwt_required
    @cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=False, type=str, help='missing "name" argument')
        parser.add_argument('id', required=False, type=str, help='missing "id" argument')

        _id = parser.parse_args().get('id')
        name = parser.parse_args().get('name')

        if _id and name:
            return {
                       'message': '1 query parameter expected'
                   }, 400
        elif _id:
            if Item.find_by_id(_id):
                Item.delete_item_using_id(_id)
                return {
                           'message': 'Deleted item with id {}'.format(_id)
                       }, 200
            else:
                return {
                           'message': 'unable to delete item with id {}, item not found'.format(_id)
                       }, 403
        elif name:
            _id = Item.find_by_name(name).id if Item.find_by_name(name) is not None else None
            if _id:
                Item.delete_item_using_id(_id)
                return {
                           'message': 'Deleted item with name {}'.format(name)
                       }, 200
            else:
                return {
                           'message': 'unable to delete item with name {}, item not found'.format(name)
                       }, 403
        else:
            return {
                       'message': 'missing query parameters'
                   }, 400


class AllItemsResource(Resource):

    @cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('sort', type=int, required=True, help='query parameter "sort" is required')
        sort = int(parser.parse_args().get('sort')) if parser.parse_args().get('sort') is not None else None

        if 0 <= sort <= 3:
            results = Item.find_all_items_sorted(sort)
            if results:
                return {
                           'count': len(results),
                           'items': [
                               {
                                   'id': result.id,
                                   'name': result.name,
                                   'price': result.price,
                                   'create_time': result.create_time
                               } for result in results
                           ]
                       }, 200
            else:
                return {
                           'message': 'no items found in database'
                       }, 404
        else:
            return {
                       'message': 'sort value out of range'
                   }, 403
