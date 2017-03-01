import json
from unittest import TestCase
from urllib.parse import urlparse

from usb import create_application
from usb.models import db


class APITestCase(TestCase):

    def setUp(self):
        self.app = create_application('config/test.py')
        self.client = self.app.test_client()

        db.app = self.app
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def _post_json(self, url, data):
        return self.client.post(url, data=json.dumps(data), content_type='application/json')

    def _patch_json(self, url, data):
        return self.client.patch(url, data=json.dumps(data), content_type='application/json')

    def assertShortIdFormat(self, short_id):
        self.assertRegex(
            short_id,
            r'^[a-zA-Z0-9]{{{min_length},}}$'.format(
                min_length=self.app.config['SHORT_URL_MIN_LENGTH']
            )
        )

    def assertShortURL(self, short_url):
        url = urlparse(short_url)
        self.assertEqual(url.scheme, 'http')
        self.assertEqual(url.netloc, self.app.config['SHORT_URL_DOMAIN'])
        self.assertEqual(url.path.count('/'), 1)
        self.assertFalse(url.params)
        self.assertFalse(url.query)
        self.assertFalse(url.fragment)

