from hashids import Hashids


class Shortener(object):

    def __init__(self, secret, min_length, short_url_domain):
        self.secret = secret
        self.min_length = min_length
        self.short_url_domain = short_url_domain
        self._hasher = Hashids(self.secret, self.min_length)

    def get_short_id(self, number):
        return self._hasher.encode(number)

    def get_short_url(self, short_id):
        return f'http://{self.short_url_domain}/{short_id}'
