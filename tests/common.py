import string
import random
from requests import Response

API_URL = 'https://flaskapp.osc-fr1.scalingo.io'
API_VERSION = 'api/v1'


def compose_response_msg(response: Response):
    req = response.request
    req_body = ''
    if isinstance(req.body, str):
        req_body = req.body
    elif isinstance(req.body, bytearray) or isinstance(req.body, bytes):
        req_body = req.body.decode(encoding='utf8')

    request_id = req.headers.get('X-Request-Id', '')

    return 'Request(id: {request_id}) \n  {method} {url} {req_body} RETURNS \n  Response [{status}] {resp_body}' \
        .format(request_id=request_id,
                method=req.method,
                url=response.url,
                req_body=req_body,
                status=response.status_code,
                resp_body=response.text)


def generate_random_name():
    random_str = '{}{}{}'.format(
        string.ascii_letters[random.randint(0, 26)],
        string.ascii_letters[random.randint(0, 26)],
        string.ascii_letters[random.randint(0, 26)]
    )
    return random_str


def generate_random_price():
    return random.randint(0, 100)








