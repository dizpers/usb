from abc import ABCMeta


class IShortener(object):

    __metaclass__ = ABCMeta

    def get_short_id(self, number):
        """
        Get short id by given integer number
        :param number: Number to be hashed
        :type number: int
        :return: String representation of the calculated hash
        :rtype: str
        """
        raise NotImplementedError

    def get_short_url(self, short_id):
        """
        Get short URL by given short id
        :param short_id: String, representing the short id
        :type short_id: str
        :return: Absolute URL calculated with given short id
        :rtype: str
        """
        raise NotImplementedError
