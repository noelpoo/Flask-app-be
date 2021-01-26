import string
import random

API_URL = 'https://flaskapp.osc-fr1.scalingo.io'


def generate_random_name():
    random_str = '{}{}{}{}'.format(
        string.ascii_letters(random.randint(26)),
        string.ascii_letters(random.randint(26)),
        string.ascii_letters(random.randint(26)),
        string.ascii_letters(random.randint(26))
    )
    return random_str


def generate_random_price():
    return random.randint(0, 100)








