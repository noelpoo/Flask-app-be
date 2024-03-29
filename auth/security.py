from werkzeug.security import safe_str_cmp
from models.user import User

users = [
    User(1, 'poosk', '1234'),
    User(2, 'noel', '1234')
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}


def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)



