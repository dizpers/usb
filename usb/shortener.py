import time

from flask import current_app

from hashids import Hashids


hashids = Hashids('asfda', 8)


def get_short_id():
    return hashids.encode(int(time.time() * 10**7))


def get_short_url(short_id):
    return f'http://{current_app.config["SERVER_NAME"]}/{short_id}'
