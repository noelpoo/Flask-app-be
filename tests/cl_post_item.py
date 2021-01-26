from serverApi import ServerApi
from common import *


def post_item(client: ServerApi, item_name, price):
    resp = client.post_item(item_name=item_name, price=price)
    if resp.status_code != 201:
        print('failed to post item! {}'.format(compose_response_msg(resp)))
        return
    print('post item success')


def login(client: ServerApi, username, password):
    resp = client.login(username, password)
    if resp.status_code != 200:
        print('failed to login!{}'.format(compose_response_msg(resp)))
    print('login success')


def main():
    for _ in range(50):
        client = ServerApi(API_URL, API_VERSION)
        login(client, 'noel', '1234')
        post_item(client, generate_random_name(), generate_random_price())


if __name__ == '__main__':
    main()


