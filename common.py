API_VERSION = 'v1'
API_PATH = '/api/{}'.format(API_VERSION)
PROJECT_ID = 'item-app-c5681'
FIREBASE_KEY_PATH = './firebase/item-app-d4e6f69fdfa1.json'

ITEM_FB_DB = "items"

SORT_MAP = {
    0: {
        'key': 'create_time',
        'desc': True
    },
    1: {
        'key': 'create_time',
        'desc': False
    },
    2: {
        'key': 'price',
        'desc': True
    },
    3: {
        'key': 'price',
        'desc': False
    },
}
