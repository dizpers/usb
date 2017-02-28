import time

from hashids import Hashids


hash = Hashids('asfda', 8)


def get_short_id():
    return hash.encode(int(time.time() * 10**7))


def get_short_url(short_id):
    return 'http://jooraccess.com/{0}'.format(short_id)
