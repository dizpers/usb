from abc import ABCMeta


class IShortener(object):

    __metaclass__ = ABCMeta

    def encode(self, number):
        """
        Get short string id by given integer number
        :param number: Number to be hashed
        :type number: int
        :return: String representation of the calculated hash
        :rtype: str
        """
        raise NotImplementedError

    def decode(self, hashed_value):
        """
        Get original value by decoding hashed one
        :param hashed_value: Encoded value
        :type hashed_value: str
        :return: Decoded value
        :rtype: int
        """
        raise NotImplementedError
