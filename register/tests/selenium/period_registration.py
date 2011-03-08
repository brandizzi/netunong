import unittest2 as unittest
from register.tests.selenium import SeleniumTestCase, ROOT_URL

class RegisterTestCase(SeleniumTestCase):

    def register_period(self):
        self.load_default_model_values()
        self.login()
        self.assertLoginOk()

        self.wait(1)    
        intention_input = self.browser().find_element_by_xpath("//input[@name='intention']")
        intention_input.send_keys("Doing something")
        task_input = self.browser().find_element_by_xpath("//select[@name='task']")
        task_input.send_keys("Test employee")
        submit = self.browser().find_element_by_xpath("//input[@type='submit']")
        submit.click()
        self.wait(1)

        period = self.employee.last_working_period
        self.assertEqual(period.intended, "Doing something")
        self.assertEqual(period.intended_task, self.task)
        self.assertFalse(period.is_complete)         
        
        self.logout()

    def setUp(self):
        self.clear_database()

registerLoginTestSuite = unittest.TestSuite()
registerLoginTestSuite.addTest(RegisterTestCase('register_period'))
#registerLoginTestSuite.addTest(RegisterTestCase('loginOk'))
