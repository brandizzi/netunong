import unittest2 as unittest
from selenium import webdriver

class SeleniumLoginTestCase(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()

    def loginFailed(self):
        self.browser.get('http://localhost:8000/netunong/')
        self.assertTrue(self.browser.find_element_by_name('username') != None)
        self.assertTrue(self.browser.find_element_by_name('password') != None);

    def tearDown(self):
        self.browser.close()

seleniumLoginTestSuite = unittest.TestSuite()
seleniumLoginTestSuite.addTest(SeleniumLoginTestCase('loginFailed'))
