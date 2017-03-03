from hashids import Hashids

from usb.interfaces import IShortener


class Shortener(IShortener):

    def __init__(self, secret, min_length, short_url_domain):
        """
        :param secret: String used in hashing process
        :type secret: str
        :param min_length: Minimal length of hash string
        :type min_length: int
        :param short_url_domain: The domain to be used for building short URLs
        :type short_url_domain: str
        """
        self.secret = secret
        self.min_length = min_length
        self.short_url_domain = short_url_domain
        self._hasher = Hashids(self.secret, self.min_length)

    def get_short_id(self, number):
        """
        Get short id by given integer number
        :param number: Number to be hashed
        :type number: int
        :return: String representation of the calculated hash
        :rtype: str
        """
        return self._hasher.encode(number)

    def get_short_url(self, short_id):
        """
        Get short URL by given short id
        :param short_id: String, representing the short id
        :type short_id: str
        :return: Absolute URL calculated with given short id
        :rtype: str
        """
        return f'http://{self.short_url_domain}/{short_id}'
