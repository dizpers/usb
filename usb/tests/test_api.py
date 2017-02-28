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

    def _post(self, url, data):
        return self.client.post(url, data=json.dumps(data), content_type='application/json')

    def assertShortIdFormat(self, short_id):
        self.assertRegex(short_id, r'^[a-zA-Z0-9]{8,}$')

    def assertShortURL(self, short_url):
        url = urlparse(short_url)
        self.assertEqual(url.scheme, 'http')
        self.assertEqual(url.netloc, self.app.config['SERVER_NAME'])
        self.assertEqual(url.path.count('/'), 1)
        self.assertFalse(url.params)
        self.assertFalse(url.query)
        self.assertFalse(url.fragment)

    def test_redirect_from_index_namespace(self):
        pass

    def test_redirect_from_links_namespace(self):
        pass

    def test_create_short_link(self):
        long_url = 'https://www.youtube.com/watch?v=Y21VecIIdBI'
        response = self._post('/links', {'url': long_url})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        data = json.loads(response.data)
        self.assertIn('url', data)
        short_url = data['url']
        self.assertNotEqual(long_url, short_url)
        self.assertShortURL(short_url)
        short_id = short_url.split('/')[-1]
        self.assertShortIdFormat(short_id)

    def test_create_short_link_for_already_shortened(self):
        long_url = 'https://www.youtube.com/watch?v=Y21VecIIdBI'
        response = self._post('/links', {'url': long_url})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        data_from_first_call = json.loads(response.data)
        self.assertIn('url', data_from_first_call)
        short_url = data_from_first_call['url']
        self.assertNotEqual(long_url, short_url)
        self.assertShortURL(short_url)
        short_id = short_url.split('/')[-1]
        self.assertShortIdFormat(short_id)
        response = self._post('/links', {'url': long_url})
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        data_from_second_call = json.loads(response.data)
        self.assertEqual(data_from_first_call, data_from_second_call)

    def test_update_short_link(self):
        pass

    def test_get_list_of_short_links(self):
        pass

    def test_get_list_of_short_links_empty_db(self):
        response = self.client.get('/links')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        data = json.loads(response.data)
        self.assertEqual(data, {})
