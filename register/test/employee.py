import unittest
from register.models import Employee
from django.contrib import auth

class CreateEmployee(unittest.TestCase):

    def __init__(self, methodName='runTest'):
        unittest.TestCase.__init__(self, methodName)
        

    def runTest(self):
        employee = Employee.create_employee(
                username="test", first_name="Test", last_name="Testein",
                middle_name="Testos", email="test@test.tst", password="test")

        user = auth.authenticate(username='test', password='test')
        self.assertNotEquals(user, None, "User should be created")

        self.assertEquals(user.first_name, "Test")
        self.assertEquals(user.last_name, "Testein")
        self.assertEquals(user.email, "test@test.tst")

        employee = Employee.objects.get(user=user)
        self.assertNotEquals(employee, None, "Employee should be found")
        self.assertEquals(employee.middle_name, "Testos")

        user.delete()
        employee.delete()

class RemoveEmployee(unittest.TestCase):
    def __init__(self, methodName='runTest'):
        unittest.TestCase.__init__(self, methodName)
    def runTest(self):
        employee = Employee.create_employee(
                username="test", first_name="Test", last_name="Testein",
                middle_name="Testos", email="test@test.tst", password="test")

        user = auth.authenticate(username='test', password='test')
        self.assertNotEquals(user, None, "User should be created")
        employee = Employee.objects.get(middle_name="Testos")
        self.assertNotEquals(employee, None, "Employee should be found")

        employee.delete_with_user()

        user = auth.authenticate(username='test', password='test')
        self.assertEquals(user, None, "User should not exist anymore")

        try:        
            employee = Employee.objects.get(middle_name="Testos")
            self.fail("Employee should not be found")
        except Employee.DoesNotExist:
            pass        

class DontCreateRepeatedEmployee(unittest.TestCase):

    def __init__(self, methodName='runTest'):
        unittest.TestCase.__init__(self, methodName)

    def runTest(self):
        employee = Employee.create_employee(
                username="test", first_name="Test", last_name="Testein",
                middle_name="Testos", email="test@test.tst", password="test")
        try:
            employee = Employee.create_employee(
                    username="test", first_name="Test", last_name="Testein",
                    middle_name="Testos", email="test@test.tst", 
                    password="test")
            self.fail("Cannot create employees with repeated usernames")
        except:
            pass
        finally:
            employee.delete_with_user()


employeeTestSuite = unittest.TestSuite()
employeeTestSuite.addTest(CreateEmployee())
employeeTestSuite.addTest(RemoveEmployee())
employeeTestSuite.addTest(DontCreateRepeatedEmployee())

