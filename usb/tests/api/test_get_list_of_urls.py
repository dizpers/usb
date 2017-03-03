from datetime import datetime
import json

from usb.models import db, DesktopRedirect, TabletRedirect, MobileRedirect
from usb.tests.base import APITestCase


class GetListOfUrls(APITestCase):

    def test_get_list_of_urls(self):
        dt = datetime.now()
        dt_str = dt.isoformat()
        redirects = (
            DesktopRedirect('aaaaaaaa', 'http://domain1.com/path?q=a', dt, 10),
            TabletRedirect('aaaaaaaa', 'http://tablet.domain1.com/path?q=a', dt, 20),
            MobileRedirect('aaaaaaaa', 'http://mobile.domain1.com/path?q=a', dt, 30),
            DesktopRedirect('bbbbbbbb', 'http://domain2.com/path/b', dt, 40),
            TabletRedirect('bbbbbbbb', 'http://tablet.domain2.com/path/b', dt, 5),
            MobileRedirect('bbbbbbbb', 'http://mobile.domain2.com/path/b', dt, 15),
            DesktopRedirect('cccccccc', 'http://domain1.com/path?q=a', dt, 1),
            TabletRedirect('cccccccc', 'http://domain1.com/path?q=a', dt, 2),
            MobileRedirect('cccccccc', 'http://domain1.com/path?q=a', dt, 3)
        )
        for redirect in redirects:
            db.session.add(redirect)
        db.session.commit()

        response = self.client.get('/urls')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        data = json.loads(response.data)
        self.assertEqual(data, {
            'aaaaaaaa': [
                {'type': 'desktop', 'url': 'http://domain1.com/path?q=a', 'redirects': 10, 'datetime': dt_str},
                {'type': 'tablet', 'url': 'http://tablet.domain1.com/path?q=a', 'redirects': 20, 'datetime': dt_str},
                {'type': 'mobile', 'url': 'http://mobile.domain1.com/path?q=a', 'redirects': 30, 'datetime': dt_str}
            ],
            'bbbbbbbb': [
                {'type': 'desktop', 'url': 'http://domain2.com/path/b', 'redirects': 40, 'datetime': dt_str},
                {'type': 'tablet', 'url': 'http://tablet.domain2.com/path/b', 'redirects': 5, 'datetime': dt_str},
                {'type': 'mobile', 'url': 'http://mobile.domain2.com/path/b', 'redirects': 15, 'datetime': dt_str}
            ],
            'cccccccc': [
                {'type': 'desktop', 'url': 'http://domain1.com/path?q=a', 'redirects': 1, 'datetime': dt_str},
                {'type': 'tablet', 'url': 'http://domain1.com/path?q=a', 'redirects': 2, 'datetime': dt_str},
                {'type': 'mobile', 'url': 'http://domain1.com/path?q=a', 'redirects': 3, 'datetime': dt_str}
            ]
        })

    def test_get_list_of_urls_empty_db(self):
        response = self.client.get('/urls')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        data = json.loads(response.data)
        self.assertEqual(data, {})
