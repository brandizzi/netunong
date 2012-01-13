from time import sleep

from test_utilities import SplinterTestCase, ModelTestCase, \
        get_organization_project_task, get_employee
from register.models import Project

from register.models import Employee

class RegisterAppTestCase(SplinterTestCase,ModelTestCase):


    def test_login(self):
        self.login()

        self.assertTrue(self.browser.is_element_present_by_name("logout"))
        self.browser.find_by_name("logout").first.click()

        self.assertTrue(self.browser.is_element_present_by_name("username"))
        self.assertTrue(self.browser.is_element_present_by_name("password"))

    def test_erasing_wp_ask_for_confirmation(self):
        self.login()

        self.browser.fill('intention', 'Ask for confirmation before erasing wp')
        self.browser.find_by_id('submit').click()
        self.assertEquals(1, self.employee.workingperiod_set.count())
        wp = self.employee.last_working_period
        self.assertEquals('Ask for confirmation before erasing wp', wp.intended)

        self.browser.find_by_id("manage").click()
        self.browser.find_by_name("delete%d"%wp.id).click()

        self.browser.get_alert()._alert.dismiss()
        wp = self.employee.last_working_period
        self.assertEquals('Ask for confirmation before erasing wp', wp.intended)

        self.browser.find_by_name("delete%d"%wp.id).click()
        self.browser.get_alert().accept()
        sleep(0.1)
        self.assertFalse(
                self.browser.is_element_present_by_tag('input', wait_time=2))
        self.assertEquals(0, self.employee.workingperiod_set.count())
        


    def login(self):
        self.browser.visit(self.home)
        self.browser.fill('username', 'test')
        self.browser.fill('password', 'test')
        self.browser.find_by_xpath("//input[@type='submit']").first.click()

        
    def setUp(self):
        SplinterTestCase.setUp(self)
        ModelTestCase.setUp(self)
        (
            self.organization, 
            self.project,
            self.task
        ) = get_organization_project_task()
        self.employee = get_employee(self.organization)

    def tearDown(self):
        SplinterTestCase.tearDown(self)
        ModelTestCase.tearDown(self)

