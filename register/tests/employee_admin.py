from django.http import HttpRequest
from django.forms import ModelForm
from django.contrib.auth.models import User

from register.models import Employee
from register.admin import EmployeeAdmin
from register.forms import EmployeeAdminForm

from test_utilities import ModelTestCase, get_organization

class EmployeeAdminTestCase(ModelTestCase):

    def test_save_new_employee_new_user(self):
        admin = EmployeeAdmin(Employee, None)

        initial = {}
        initial['first_name'] = 'Fulano'
        initial['middle_name'] = 'de'
        initial['last_name'] = 'Tal'
        initial['username'] = 'fulano.tal'
        initial['email'] = 'fulano@tal.com'
        initial['password'] = 'fulanopass'
        initial['organization'] = self.organization.id

        request = HttpRequest()
        form = EmployeeAdminForm(initial)
        form.is_valid()
        self.assertTrue(form.is_valid())
        employee = Employee()
        
        admin.save_model(request, employee, form, False)

        retrieved = Employee.objects.get(middle_name='de')

        self.assertEquals(initial['first_name'], retrieved.user.first_name)
        self.assertEquals(initial['middle_name'], retrieved.middle_name)
        self.assertEquals(initial['last_name'], retrieved.user.last_name)
        self.assertEquals(initial['username'], retrieved.user.username)
        self.assertEquals(initial['email'], retrieved.user.email)
        self.assertEquals(self.organization, retrieved.organization)
        

    def setUp(self):
        ModelTestCase.setUp(self)
        self.organization = get_organization()

    def tearDown(self):
        ModelTestCase.tearDown(self)

