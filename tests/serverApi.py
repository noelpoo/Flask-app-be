import requests


class ServerApi:
    def __init__(self, server_url, api_version):
        self.server_url = server_url
        self.api_version = api_version
        self.access_token = ''
        self.is_logged_in = False

    def login(self, username='noel', password='1234'):
        api_url = '{}/auth'.format(self.server_url)
        payload = {
            "username": username,
            "password": password
        }
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        resp = requests.post(api_url, json=payload, headers=headers, verify=False)
        if resp.status_code != 200:
            return resp
        else:
            resp_json= resp.json()
            token = resp_json.get('access_token', "")
            self.access_token = 'JWT {}'.format(token)
            return self.access_token

    # login required
    def post_item(self, item_name, price):
        api_url = '{}/{}/item'.format(self.server_url, self.api_version)
        payload = {
            "name": item_name,
            "price": price
        }
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            'Authorization': self.access_token
        }
        return requests.post(api_url, json=payload, headers=headers, verify=False)

    def get_item(self, item_name):
        api_url = '{}/item/{}'.format(self.server_url, item_name)
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json'
        }
        return requests.post(api_url, headers=headers, verify=False)

    # login required
    def delete_item(self, item_name):
        api_url = '{}/item/{}'.format(self.server_url, item_name)
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            'Authorization': self.access_token
        }
        return requests.delete(api_url, headers=headers, verify=False)