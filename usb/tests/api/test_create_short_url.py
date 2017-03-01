import json

from usb.tests.base import APITestCase


class CreateShortURLTestCase(APITestCase):

    def test_create_short_url(self):
        long_url = 'https://www.youtube.com/watch?v=Y21VecIIdBI'

        response = self._post_json('/urls', {'url': long_url})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        data = json.loads(response.data)
        self.assertIn('url', data)
        short_url = data['url']
        self.assertNotEqual(long_url, short_url)
        self.assertShortURL(short_url)
        short_id = short_url.split('/')[-1]
        self.assertShortIdFormat(short_id)

    def test_create_short_url_for_already_shortened_url(self):
        long_url = 'https://www.youtube.com/watch?v=Y21VecIIdBI'

        response = self._post_json('/urls', {'url': long_url})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        data_from_first_call = json.loads(response.data)
        self.assertIn('url', data_from_first_call)
        short_url = data_from_first_call['url']
        self.assertNotEqual(long_url, short_url)
        self.assertShortURL(short_url)
        short_id = short_url.split('/')[-1]
        self.assertShortIdFormat(short_id)

        response = self._post_json('/urls', {'url': long_url})

        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        data_from_second_call = json.loads(response.data)
        self.assertEqual(data_from_first_call, data_from_second_call)
