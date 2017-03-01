from usb.tests.base import APITestCase


class RedirectFromShortURLTestCase(APITestCase):

    def _test_redirect_desktop(self, url):
        pass

    def _test_redirect_tablet(self, url):
        pass

    def _test_redirect_mobile(self, url):
        pass

    def _test_redirect(self, url):
        self._test_redirect_desktop(url)
        self._test_redirect_tablet(url)
        self._test_redirect_mobile(url)

    def test_redirect_from_index_namespace(self):
        self._test_redirect('/')

    def test_redirect_from_links_namespace(self):
        self._test_redirect('/urls/')

