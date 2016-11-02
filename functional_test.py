#coding = utf-8
from django.test import LiveServerTestCase
from selenium import webdriver

__author__='yangli'

class UserPageTest (LiveServerTestCase):
    browser = None

    @classmethod
    def setUpClass(cls):
        super(UserPageTest, cls).setUpClass()
        cls.browser = webdriver.PhantomJS()
        cls.username = os.environ.get('username','')
        cls.password = os.environ.get('password','')

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(UserPageTest, cls).tearDownClass()

    def test_bind_user(self):
        self.browser.get('%s%s' % (self.live_server_url, '/u/bind/'))

        name_box = self.browser.find_element_by_id('inputUsername')
        name_box.send_keys(self.username)

        password_box = self.browser.find_element_by_id('inputPassword')
        password_box.send_keys(self.password)

        submit_button = self.browser.find_element_by_id('#validationHolder > button')
        submit_button.click()

        self.assertIn('认证成功', self.browser.find_element_by_id('mainbody').text)
