from django.http import HttpRequest
from django.forms import ModelForm
from django.contrib.auth.models import User

from register.models import Employee
from register.admin import EmployeeAdmin
from register.forms import EmployeeAdminForm

from test_utilities import ModelTestCase, get_organization

class EmployeeAdminTestCase(ModelTestCase):

    def test_save_new_employee(self):
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

    def test_update_employee(self):
        admin = EmployeeAdmin(Employee, None)
        employee = Employee.create_employee(organization=self.organization,
                    username="cicrano.tal", first_name="Cicrano", last_name="Tal",
                    middle_name="de", email="cicrano@de.tal", 
                    password="cicr")

        initial = {}
        initial['first_name'] = 'Beltrano'
        initial['middle_name'] = 'de'
        initial['last_name'] = 'Tal'
        initial['username'] = 'fulano.tal'
        initial['email'] = 'beltrano@tal.com'
        initial['password'] = 'beltr'
        initial['organization'] = self.organization.id

        request = HttpRequest()
        form = EmployeeAdminForm(initial)
        self.assertTrue(form.is_valid())
        
        admin.save_model(request, employee, form, True)

        retrieved = Employee.objects.get(middle_name='de')

        self.assertEquals(initial['first_name'], retrieved.user.first_name)
        self.assertEquals(initial['middle_name'], retrieved.middle_name)
        self.assertEquals(initial['last_name'], retrieved.user.last_name)
        self.assertEquals(initial['username'], retrieved.user.username)
        self.assertEquals(initial['email'], retrieved.user.email)
        self.assertEquals(self.organization, retrieved.organization)

    def test_update_employee_no_passwd(self):
        admin = EmployeeAdmin(Employee, None)
        employee = Employee.create_employee(organization=self.organization,
                    username="cicrano.tal", first_name="Cicrano", last_name="Tal",
                    middle_name="de", email="cicrano@de.tal", 
                    password="cicr")

        initial = {}
        initial['first_name'] = 'Beltrano'
        initial['middle_name'] = 'de'
        initial['last_name'] = 'Tal'
        initial['username'] = 'fulano.tal'
        initial['email'] = 'beltrano@tal.com'
        #initial['password'] = 'beltr'
        initial['organization'] = self.organization.id
        request = HttpRequest()
        form = EmployeeAdminForm(initial, instance=employee)
        self.assertTrue(form.is_valid())
        
        admin.save_model(request, employee, form, True)

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

