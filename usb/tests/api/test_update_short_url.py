from datetime import datetime
import json

from usb.models import db, Desktop, Tablet, Mobile
from usb.tests.base import APITestCase


class UpdateShortUrlTestCase(APITestCase):

    def setUp(self):
        super(UpdateShortUrlTestCase, self).setUp()

        self.dt = datetime.now()
        redirects = (
            Desktop('aaaaaaaa', 'http://domain1.com/path?q=a', self.dt, 10),
            Tablet('aaaaaaaa', 'http://tablet.domain1.com/path?q=a', self.dt, 20),
            Mobile('aaaaaaaa', 'http://mobile.domain1.com/path?q=a', self.dt, 30)
        )

        for redirect in redirects:
            db.session.add(redirect)

        db.session.commit()

    def test_update_short_url(self):
        response = self._patch_json('/urls/aaaaaaaa', {'tablet': 'http://gov.us/elect/president?name='})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        data = json.loads(response.data)
        self.assertEqual(data, {})

        tablet_redirects = Tablet.query.filter_by(short='aaaaaaaa').all()
        self.assertEqual(len(tablet_redirects), 1)
        tablet_redirect = tablet_redirects[0]
        self.assertEqual(tablet_redirect.short, 'aaaaaaaa')
        # TODO: get device code from actual class?
        self.assertEqual(tablet_redirect.type, 'tablet')
        self.assertEqual(tablet_redirect.url, 'http://gov.us/elect/president?name=')
        self.assertEqual(tablet_redirect.count, 0)
        self.assertNotEqual(tablet_redirect.datetime, self.dt)

    def test_update_short_url_no_such_short_id(self):
        response = self._patch_json('/urls/bbb', {'tablet': 'http://gov.us/elect/president?name='})

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        data = json.loads(response.data)
        self.assertEqual(data, {})

