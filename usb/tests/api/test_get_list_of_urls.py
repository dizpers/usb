from datetime import datetime
import json

from usb.models import db, DeviceType, Redirect
from usb.tests.base import APITestCase


class GetListOfUrls(APITestCase):

    def test_get_list_of_urls(self):
        dt = datetime.now()
        dt_str = dt.isoformat()
        redirects = [
            Redirect('aaaaaaaa', DeviceType.DESKTOP, 'http://domain1.com/path?q=a', count=10, datetime=dt),
            Redirect('aaaaaaaa', DeviceType.TABLET, 'http://tablet.domain1.com/path?q=a', count=20, datetime=dt),
            Redirect('aaaaaaaa', DeviceType.MOBILE, 'http://mobile.domain1.com/path?q=a', count=30, datetime=dt),
            Redirect('bbbbbbbb', DeviceType.DESKTOP, 'http://domain2.com/path/b', count=40, datetime=dt),
            Redirect('bbbbbbbb', DeviceType.TABLET, 'http://tablet.domain2.com/path/b', count=5, datetime=dt),
            Redirect('bbbbbbbb', DeviceType.MOBILE, 'http://mobile.domain2.com/path/b', count=15, datetime=dt),
            Redirect('cccccccc', DeviceType.DESKTOP, 'http://domain1.com/path?q=a', count=1, datetime=dt),
            Redirect('cccccccc', DeviceType.TABLET, 'http://domain1.com/path?q=a', count=2, datetime=dt),
            Redirect('cccccccc', DeviceType.MOBILE, 'http://domain1.com/path?q=a', count=3, datetime=dt)
        ]
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
