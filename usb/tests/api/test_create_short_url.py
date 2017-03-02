import json

from usb.tests.base import APITestCase


class CreateShortURLTestCase(APITestCase):

    def setUp(self):
        super(CreateShortURLTestCase, self).setUp()
        self.long_url = 'https://www.youtube.com/watch?v=Y21VecIIdBI'

    def _validate_response(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

    def _validate_data(self, data):
        self.assertIn('url', data)
        short_url = data['url']
        self.assertNotEqual(self.long_url, short_url)
        self.assertShortURL(short_url)
        short_id = short_url.split('/')[-1]
        self.assertShortIdFormat(short_id)
        # TODO: maybe not to return it here?
        return short_id

    def test_create_short_url(self):
        response = self._post_json('/urls', {'url': self.long_url})
        self._validate_response(response)

        data = json.loads(response.data)
        self._validate_data(data)

    def test_create_short_url_for_already_shortened_url(self):

        response = self._post_json('/urls', {'url': self.long_url})
        self._validate_response(response)

        data = json.loads(response.data)
        short_id_first = self._validate_data(data)

        response = self._post_json('/urls', {'url': self.long_url})
        self._validate_response(response)

        data = json.loads(response.data)
        short_id_second = self._validate_data(data)

        self.assertNotEqual(short_id_first, short_id_second)
