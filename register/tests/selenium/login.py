import unittest2 as unittest
from . import SeleniumTestCase, ROOT_URL

from register.tests.test_utilities import clear_database,\
         get_organization_project_task, get_employee

class LoginTestCase(SeleniumTestCase):

    def loginFailed(self):
        self.login(username='non-existent user', password='invalid passwerd')

        message = self.browser().find_element_by_class_name('error')
        self.assertIsNotNone(message)
        self.assertEqual(self.browser().current_url, ROOT_URL+'login/')

    def loginOk(self):
        clear_database()
        self.load_default_model_values()
        self.login()
        self.assertLoginOk()
        self.logout()
        clear_database()

seleniumLoginTestSuite = unittest.TestSuite()
seleniumLoginTestSuite.addTest(LoginTestCase('loginFailed'))
seleniumLoginTestSuite.addTest(LoginTestCase('loginOk'))
