from unittest import TestCase

from usb.shortener import shorten


class ShortenerTestCase(TestCase):

    def test_shorten(self):
        long_url = 'https://www.youtube.com/watch?v=Y21VecIIdBI'
        short_url = shorten(long_url)
        self.assertNotEqual(long_url, short_url)
        self.assertRegex(short_url, r'^[a-zA-Z0-9]{6,}$')
