from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token

from auth.security import *


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
