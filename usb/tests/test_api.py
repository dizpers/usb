from unittest import TestCase

from usb import create_application
from usb import config



class APITestCase(TestCase):

    def setUp(self):
        self.app = create_application(config.test)
        self.client = self.app.test_client()
        self.app.init_db()

    def tearDown(self):
        self.app.drop_db()

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
