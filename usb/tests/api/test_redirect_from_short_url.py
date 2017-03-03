from unittest.mock import patch, Mock

from usb.tests.base import APITestCase
from usb.models import db, Desktop, Tablet, Mobile


class RedirectFromShortURLTestCase(APITestCase):

    def setUp(self):
        super(RedirectFromShortURLTestCase, self).setUp()

        redirects = (
            Desktop('aaaaaaaa', 'http://domain1.com/path?q=a'),
            Tablet('aaaaaaaa', 'http://tablet.domain1.com/path?q=a'),
            Mobile('aaaaaaaa', 'http://mobile.domain1.com/path?q=a'),
            Desktop('bbbbbbbb', 'http://domain2.com/path?q=b'),
            Tablet('bbbbbbbb', 'http://tablet.domain2.com/path?q=b'),
            Mobile('bbbbbbbb', 'http://mobile.domain2.com/path?q=b')
        )

        for redirect in redirects:
            db.session.add(redirect)

        db.session.commit()

        self.PATCH_TARGET = 'usb.blueprints.api.get_device_model_from_request'

    def _test_redirect_desktop(self, url):
        with patch(self.PATCH_TARGET, return_value=Desktop):
            response = self.client.get(url + 'aaaaaaaa')
        self.assertEqual(response.status_code, self.app.config['REDIRECT_CODE'])
        self.assertEqual(response.headers['Location'], 'http://domain1.com/path?q=a')

    def _test_redirect_tablet(self, url):
        with patch(self.PATCH_TARGET, return_value=Tablet):
            response = self.client.get(url + 'aaaaaaaa')
        self.assertEqual(response.status_code, self.app.config['REDIRECT_CODE'])
        self.assertEqual(response.headers['Location'], 'http://tablet.domain1.com/path?q=a')

    def _test_redirect_mobile(self, url):
        with patch(self.PATCH_TARGET, return_value=Mobile):
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

        desktop = Desktop.query.filter_by(short='aaaaaaaa').first()
        self.assertEqual(desktop.count, 3)
        tablet = Tablet.query.filter_by(short='aaaaaaaa').first()
        self.assertEqual(tablet.count, 0)
        mobile = Mobile.query.filter_by(short='aaaaaaaa').first()
        self.assertEqual(mobile.count, 1)
