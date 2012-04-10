from django.forms import ModelForm
from django.contrib.auth.models import User

from register.models import Employee
from register.forms import EmployeeAdminForm

from test_utilities import ModelTestCase, get_organization_project_task, \
        get_employee

class EmployeeAdminFormTestCase(ModelTestCase):

    def test_init(self):
        user = User(username="fulano.tal", first_name="Fulano", last_name="Tal",
                    email="fulano@test.tst",   password="fulano")
        employee = Employee(organization=self.organization, middle_name="de",
                user=user)

        form = EmployeeAdminForm(instance=employee)
        self.assertEquals(form.initial['first_name'], employee.user.first_name)
        self.assertEquals(form.initial['middle_name'], employee.middle_name)
        self.assertEquals(form.initial['last_name'], employee.user.last_name)
        self.assertEquals(form.initial['username'], employee.user.username)
        self.assertEquals(form.initial['email'], employee.user.email)
        

    def setUp(self):
        ModelTestCase.setUp(self)
        (
            self.organization, 
            self.project,
            self.task
        ) = get_organization_project_task()
        self.employee = get_employee(self.organization)

    def tearDown(self):
        ModelTestCase.tearDown(self)

