from unittest import TestCase

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

    def test_redirect_from_index_namespace(self):
        pass

    def test_redirect_from_links_namespace(self):
        pass

    def test_create_short_link(self):
        pass

    def test_update_short_link(self):
        pass

    def get_list_of_short_links(self):
        pass
