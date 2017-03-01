from unittest.mock import patch, Mock

from usb.tests.base import APITestCase
from usb.models import db, Redirect, DeviceType


class RedirectFromShortURLTestCase(APITestCase):

    def setUp(self):
        super(RedirectFromShortURLTestCase, self).setUp()

        redirects = [
            Redirect('aaaaaaaa', DeviceType.DESKTOP, 'http://domain1.com/path?q=a'),
            Redirect('aaaaaaaa', DeviceType.TABLET, 'http://tablet.domain1.com/path?q=a'),
            Redirect('aaaaaaaa', DeviceType.MOBILE, 'http://mobile.domain1.com/path?q=a'),
            Redirect('bbbbbbbb', DeviceType.DESKTOP, 'http://domain2.com/path?q=b'),
            Redirect('bbbbbbbb', DeviceType.TABLET, 'http://tablet.domain2.com/path?q=b'),
            Redirect('bbbbbbbb', DeviceType.MOBILE, 'http://mobile.domain2.com/path?q=b')
        ]

        for redirect in redirects:
            db.session.add(redirect)

        db.session.commit()

        self.PATCH_TARGET = 'usb.utils.get_device_type'

    def _test_redirect_desktop(self, url):
        with patch(self.PATCH_TARGET, Mock(return_value=DeviceType.DESKTOP)):
            response = self.client.get(url + 'aaaaaaaa')
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response.headers['Location'], 'http://domain1.com/path?q=a')

    def _test_redirect_tablet(self, url):
        with patch(self.PATCH_TARGET, Mock(return_value=DeviceType.TABLET)):
            response = self.client.get(url + 'aaaaaaaa')
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response.headers['Location'], 'http://tablet.domain1.com/path?q=a')

    def _test_redirect_mobile(self, url):
        with patch(self.PATCH_TARGET, Mock(return_value=DeviceType.MOBILE)):
            response = self.client.get(url + 'aaaaaaaa')
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response.headers['Location'], 'http://mobile.domain1.com/path?q=a')

    def _test_redirect(self, url):
        self._test_redirect_desktop(url)
        self._test_redirect_tablet(url)
        self._test_redirect_mobile(url)

    def test_redirect_from_index_namespace(self):
        self._test_redirect('/')

    def test_redirect_from_links_namespace(self):
        self._test_redirect('/urls/')
