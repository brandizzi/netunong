import time
import subprocess
import unittest2 as unittest

from selenium import webdriver
from selenium.webdriver.common.exceptions import NoSuchElementException

from register.models import Organization, Project, Employee, Task, WorkingPeriod
from django.contrib.auth.models import User
from register.tests.test_utilities import clear_database,\
         get_organization_project_task, get_employee

import settings

ROOT_URL = 'http://localhost:8000/netunong/'

class SeleniumTestCase(unittest.TestCase):

    def setUp(self):
        self._browser = webdriver.Chrome()

    def tearDown(self):
        self._browser.quit()

    def browser(self, browser_class=webdriver.Chrome):
        return self._browser

    def wait(self, seconds):
        time.sleep(seconds)

    def load_default_model_values(self):
        ##clear_database()
        subprocess.call(['./usertest.py'])
        self.organization = Organization.objects.all()[0]
        self.project = Project.objects.all()[0]
        self.employee = Employee.objects.all()[0]
        self.task = Task.objects.all()[0]

    def clear_database(self):
        clear_database()

    def load_login_stuff(self):
        self.browser().get(ROOT_URL)
        time.sleep(1)
        self.login_form = self.browser().find_element_by_xpath("//form[@name='login']")
        self.username = self.browser().find_element_by_name('username')
        self.password = self.browser().find_element_by_name('password')

        self.assertIsNotNone(self.username)
        self.assertIsNotNone(self.password)
        self.assertIsNotNone(self.login_form)

    def login(self, username=None, password=None):
        self.load_login_stuff()
        if username is None:
            username = self.employee.user.username
        if password is None:
            password = 'test'
        self.username.send_keys(username)
        self.password.send_keys(password)
        self.login_form.submit()
        time.sleep(1)

    def assertLoginOk(self):
        with self.assertRaises(NoSuchElementException):
            message = self.browser().find_element_by_class_name('error')
        self.assertEqual(self.browser().current_url, ROOT_URL)

    def logout(self):
        logout_link = self.browser().find_element_by_id('logout')
        self.assertIsNotNone(logout_link)
        logout_link.click()
        time.sleep(1)

