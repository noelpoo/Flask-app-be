import os
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from models.item import ItemResource, AllItemsResource
from auth.login import UserLogin


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

# ENDPOINTS
api.add_resource(ItemResource, '{}/item'.format(API_PATH))
api.add_resource(AllItemsResource, '{}/items'.format(API_PATH))
api.add_resource(UserLogin, '{}/login'.format(API_PATH))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)



