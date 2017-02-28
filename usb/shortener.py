import time

from flask import current_app

from hashids import Hashids


def get_hasher(secret, min_length):
    if not hasattr(get_hasher, 'hasher'):
        get_hasher.hasher = Hashids(secret, min_length)
    return get_hasher.hasher


def get_short_id():
    hasher = get_hasher(
        current_app.config['HASHIDS_SECRET'],
        current_app.config['SHORT_URL_MIN_LENGTH']
    )
    return hasher.encode(int(time.time() * 10**7))


def get_short_url(short_id):
    return f'http://{current_app.config["SHORT_URL_DOMAIN"]}/{short_id}'
