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

        self.PATCH_TARGET = 'usb.blueprints.api.get_device_type'

    def _test_redirect_desktop(self, url):
        with patch(self.PATCH_TARGET, return_value=DeviceType.DESKTOP):
            response = self.client.get(url + 'aaaaaaaa')
        self.assertEqual(response.status_code, self.app.config['REDIRECT_CODE'])
        self.assertEqual(response.headers['Location'], 'http://domain1.com/path?q=a')

    def _test_redirect_tablet(self, url):
        with patch(self.PATCH_TARGET, return_value=DeviceType.TABLET):
            response = self.client.get(url + 'aaaaaaaa')
        self.assertEqual(response.status_code, self.app.config['REDIRECT_CODE'])
        self.assertEqual(response.headers['Location'], 'http://tablet.domain1.com/path?q=a')

    def _test_redirect_mobile(self, url):
        with patch(self.PATCH_TARGET, return_value=DeviceType.MOBILE):
            response = self.client.get(url + 'aaaaaaaa')
        self.assertEqual(response.status_code, self.app.config['REDIRECT_CODE'])
        self.assertEqual(response.headers['Location'], 'http://mobile.domain1.com/path?q=a')

    def _test_redirect(self, url):
        self._test_redirect_desktop(url)
        self._test_redirect_tablet(url)
        self._test_redirect_mobile(url)

    def test_redirect_from_index_namespace(self):
        self._test_redirect('/')

    def test_redirect_from_links_namespace(self):
        self._test_redirect('/urls/')

    def test_redirect_increase_count(self):
        # 3 desktop
        self._test_redirect_desktop('/')
        self._test_redirect_desktop('/')
        self._test_redirect_desktop('/')

        # 0 tablet

        # 1 mobile
        self._test_redirect_mobile('/')

        redirects = Redirect.query.filter_by(short='aaaaaaaa').all()
        for redirect in redirects:
            if redirect.type == DeviceType.DESKTOP:
                self.assertEqual(redirect.count, 3)
            if redirect.type == DeviceType.TABLET:
                self.assertEqual(redirect.count, 0)
            if redirect.type == DeviceType.MOBILE:
                self.assertEqual(redirect.count, 1)
