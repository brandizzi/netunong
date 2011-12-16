import unittest2 as unittest
from test_utilities import SplinterTestCase, get_organization_project_task, \
        get_employee

from register.models import Project

from register.models import Employee

class RegisterAppTestCase(SplinterTestCase):

    def setUp(self):
        SplinterTestCase.setUp(self)
        (
            self.organization, 
            self.project,
            self.task
        ) = get_organization_project_task()
        self.employee = get_employee(self.organization)

    def login(self):
        self.browser.visit(self.home)
        self.browser.fill('username', 'test')
        self.browser.fill('password', 'test')
        self.browser.find_by_xpath("//input[@type='submit']").first.click()

        self.assertTrue(self.browser.is_element_present_by_name("logout"))
        self.browser.find_by_name("logout").first.click()

        self.assertTrue(self.browser.is_element_present_by_name("username"))
        self.assertTrue(self.browser.is_element_present_by_name("password"))
        


    def f(s):
        self.browser.type('intention', 'Write Splinter tests')
        self.browser.select('task', str(self.task.id))
        

registerAppTestSuite = unittest.TestSuite()
registerAppTestSuite.addTest(RegisterAppTestCase('login'))
