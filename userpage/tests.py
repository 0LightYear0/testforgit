from django.test import TestCase
from django.http import HttpRequest
from django.core.urlresolvers import resolve

import userpage.urls
from codex.baseerror import InputError

class GetTest(TestCase):
    def test_get_without_openid(self):
        found = resolve('/user/bind/', urlconf=userpage.urls)
        with self.assertRaisesMessage(InputError, 'Filed "openid" required'):
            found.func(HttpRequest())
# Create your tests here.
