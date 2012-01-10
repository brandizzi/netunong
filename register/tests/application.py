from test_utilities import SplinterTestCase, ModelTestCase, \
        get_organization_project_task, get_employee

from register.models import Project

from register.models import Employee

class RegisterAppTestCase(SplinterTestCase,ModelTestCase):


    def test_login(self):
        self.browser.visit(self.home)
        self.browser.fill('username', 'test')
        self.browser.fill('password', 'test')
        self.browser.find_by_xpath("//input[@type='submit']").first.click()

        self.assertTrue(self.browser.is_element_present_by_name("logout"))
        self.browser.find_by_name("logout").first.click()

        self.assertTrue(self.browser.is_element_present_by_name("username"))
        self.assertTrue(self.browser.is_element_present_by_name("password"))
        
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

