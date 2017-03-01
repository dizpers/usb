from datetime import datetime
import json

from usb.models import db, Redirect, DeviceType
from usb.tests.base import APITestCase


class UpdateShortUrlTestCase(APITestCase):

    def test_update_short_url(self):
        dt = datetime.now()
        redirects = [
            Redirect('aaaaaaaa', DeviceType.DESKTOP, 'http://domain1.com/path?q=a', count=10, datetime=dt),
            Redirect('aaaaaaaa', DeviceType.TABLET, 'http://tablet.domain1.com/path?q=a', count=20, datetime=dt),
            Redirect('aaaaaaaa', DeviceType.MOBILE, 'http://mobile.domain1.com/path?q=a', count=30, datetime=dt)
        ]
        for redirect in redirects:
            db.session.add(redirect)
        db.session.commit()
        self._patch_json('/urls/aaaaaaaa', {'tablet': 'http://gov.us/elect/president?name='})
        tablet_redirects = Redirect.query.filter_by(short='aaaaaaaa', type=DeviceType.TABLET).all()
        self.assertTrue(tablet_redirects)
        self.assertEqual(len(tablet_redirects), 1)
        tablet_redirect = tablet_redirects[0]
        self.assertEqual(tablet_redirect.short, 'aaaaaaaa')
        self.assertEqual(tablet_redirect.type, DeviceType.TABLET)
        self.assertEqual(tablet_redirect.url, 'http://gov.us/elect/president?name=')

    def test_update_short_url_no_such_short_id(self):
        dt = datetime.now()
        redirects = [
            Redirect('aaaaaaaa', DeviceType.DESKTOP, 'http://domain1.com/path?q=a', count=10, datetime=dt),
            Redirect('aaaaaaaa', DeviceType.TABLET, 'http://tablet.domain1.com/path?q=a', count=20, datetime=dt),
            Redirect('aaaaaaaa', DeviceType.MOBILE, 'http://mobile.domain1.com/path?q=a', count=30, datetime=dt)
        ]
        for redirect in redirects:
            db.session.add(redirect)
        db.session.commit()
        response = self._patch_json('/urls/bbb', {'tablet': 'http://gov.us/elect/president?name='})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        data = json.loads(response.data)
        self.assertEqual(data, {})

