from hashids import Hashids

from usb.interfaces import IShortener


class Shortener(IShortener):

    def __init__(self, *hasher_args, **hasher_kwargs):
        """
        :param hasher_args: Positional arguments for hasher
        :param hasher_kwargs: Named arguments for hasher
        """
        self._hasher = Hashids(*hasher_args, **hasher_kwargs)

    def encode(self, number):
        """
        Get short string id by given integer number
        :param number: Number to be hashed
        :type number: int
        :return: String representation of the calculated hash
        :rtype: str
        """
        return self._hasher.encode(number)

    def decode(self, hashed_value):
        """
        Get original value by decoding hashed one
        :param hashed_value: Encoded value
        :type hashed_value: str
        :return: Decoded value
        :rtype: int
        """
        return self._hasher.decode(hashed_value)
