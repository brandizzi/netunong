import unittest2 as unittest
from . import SeleniumTestCase, ROOT_URL

class LoginTestCase(SeleniumTestCase):

    def loginFailed(self):
        #self.load_browser()
        self.login(username='non-existent user', password='invalid passwerd')

        message = self.browser().find_element_by_class_name('error')
        self.assertIsNotNone(message)
        self.assertEqual(self.browser().current_url, ROOT_URL+'login/')

    def loginOk(self):
        self.load_default_model_values()
        self.login()
        self.assertLoginOk()
        self.logout()


seleniumLoginTestSuite = unittest.TestSuite()
seleniumLoginTestSuite.addTest(LoginTestCase('loginFailed'))
seleniumLoginTestSuite.addTest(LoginTestCase('loginOk'))
