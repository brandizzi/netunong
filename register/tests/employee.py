import unittest2 as unittest
from test_utilities import ModelTestCase, clear_database

from datetime import datetime

from register.models import Employee, Organization, Task, Project, WorkingPeriod
from django.contrib import auth
from django.contrib.auth.models import User

class EmployeeTestCase(ModelTestCase):

    def __init__(self, methodName='runTest'):
        ModelTestCase.__init__(self, methodName)

    def setUp(self):
        self.organization = Organization(name="SEA Tecnologia",
                description="Criadora do Netuno Nova Geracao (NetunoNG)")
        self.organization.save()


    def create_employee(self):
        employee = self.get_default_employee()

        user = auth.authenticate(username='test', password='test')
        self.assertIsNotNone(user, "User should be created")

        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "Testein")
        self.assertEqual(user.email, "test@test.tst")

        employee = Employee.objects.get(user=user)
        self.assertIsNotNone(employee, "Employee should be found")
        self.assertEqual(employee.middle_name, "Testos")

    def detele_with_user(self):
        employee = self.get_default_employee()

        user = auth.authenticate(username='test', password='test')
        self.assertIsNotNone(user, "User should be created")
        employee = Employee.objects.get(middle_name="Testos")
        self.assertIsNotNone(employee, "Employee should be found")

        employee.delete_with_user()

        user = auth.authenticate(username='test', password='test')
        self.assertIsNone(user, "User should not exist anymore")

        with self.assertRaises(Employee.DoesNotExist):
            employee = Employee.objects.get(middle_name="Testos")

    def reject_repeated_username(self):
        employee = self.get_default_employee()
        with self.assertRaises(Exception):
            employee = Employee.create_employee(organization=self.organization,
                    username="test", first_name="Test", last_name="Testein",
                    middle_name="Testos", email="test@test.tst", 
                    password="test")

    def has_organization(self):
        organization = Organization(name="SEA Tecnologia",
                description="Criadora do Netuno Nova Geracao (NetunoNG)")
        organization.save()
        employee = Employee.create_employee(organization=organization,
                username="test", first_name="Test", last_name="Testein",
                middle_name="Testos", email="test@test.tst", password="test")

        self.assertEqual(employee.organization, organization)
        retrieved = Employee.objects.get(middle_name='Testos')
        self.assertEqual(retrieved.organization, organization)
        
    def has_tasks(self):
        employee = self.get_default_employee()

        project = Project(name="Project 1", description="First project",
                    organization=self.organization)
        project.save()
        task1 = Task(name="Task 1", description="First task", project=project)
        task2 = Task(name="Task 2", description="Second task", project=project)
        task1.save()
        task2.save()

        employee.tasks.add(task1, task2)

        retrieved = Employee.objects.get(middle_name='Testos')
        self.assertItemsEqual(retrieved.tasks.all(), (task1, task2))

    def has_working_periods(self):
        employee = self.get_default_employee()

        project = Project(name="Project 1", description="First project",
                    organization=self.organization)
        project.save()
        task = Task(name="Test employee", project=project, 
                description="Testing the Employee model")
        task.save()

        wp1 = WorkingPeriod(employee=employee,
                intended="test if employee has working period",
                intended_task=task,
                executed="made the employe have it",
                executed_task=task,
                start= datetime.now(), end=datetime.now())
        wp2 = WorkingPeriod(employee=employee,
                intended="test if employee has working period again",
                intended_task=task,
                start= datetime.now())
        wp1.save()
        wp2.save()

        self.assertItemsEqual(employee.workingperiod_set.all(), (wp1, wp2))

    def last_working_period(self):
        employee = self.get_default_employee()

        project = Project(name="Project 1", description="First project",
                    organization=self.organization)
        project.save()
        task = Task(name="Test employee", project=project, 
                description="Testing the Employee model")
        task.save()

        wp1 = WorkingPeriod(employee=employee,
                intended="test if employee has working period",
                intended_task=task,
                executed="made the employe have it",
                executed_task=task,
                start= datetime.now(), end=datetime.now())
        wp2 = WorkingPeriod(employee=employee,
                intended="test if employee has working period again",
                intended_task=task,
                start= datetime.now())
        wp1.save()
        wp2.save()

        self.assertEquals(employee.last_working_period, wp2)

    def last_working_period_none_found(self):
        employee = self.get_default_employee()

        project = Project(name="Project 1", description="First project",
                    organization=self.organization)
        project.save()
        task = Task(name="Test employee", project=project, 
                description="Testing the Employee model")
        task.save()

        self.assertIs(employee.last_working_period, WorkingPeriod.NONE)
        
    def name_properties(self):
        employee = self.get_default_employee()
        self.assertEqual(employee.first_name, employee.user.first_name)
        self.assertEqual(employee.last_name, employee.user.last_name)
        self.assertEqual(employee.name, "%s %s %s" % ( 
                    employee.first_name, employee.middle_name, employee.last_name
             ))
        
    def get_default_employee(self):
        return Employee.create_employee(organization=self.organization,
                username="test", first_name="Test", last_name="Testein",
                middle_name="Testos", email="test@test.tst", password="test")

    """def save(self):
        employee = Employee(username='test', password='test', first_name='Test', 
            middle_name='Testos', last_name='Testein', email="test@test.tst",
            organization=self.organization)
        employee.save()

        
        user = auth.authenticate(username='test', password='test')
        self.assertIsNotNone(user, "User should be created")

        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "Testein")
        self.assertEqual(user.email, "test@test.tst")

        employee = Employee.objects.get(user=user)
        self.assertIsNotNone(employee, "Employee should be found")
        self.assertEqual(employee.middle_name, "Testos")

        self.assertEqual(employee.user, user)"""


    def tearDown(self):
        clear_database()


employeeTestSuite = unittest.TestSuite()
employeeTestSuite.addTest(EmployeeTestCase('create_employee'))
employeeTestSuite.addTest(EmployeeTestCase('detele_with_user'))
employeeTestSuite.addTest(EmployeeTestCase('reject_repeated_username'))
employeeTestSuite.addTest(EmployeeTestCase('has_organization'))
employeeTestSuite.addTest(EmployeeTestCase('has_tasks'))
employeeTestSuite.addTest(EmployeeTestCase('has_working_periods'))
employeeTestSuite.addTest(EmployeeTestCase('last_working_period'))
employeeTestSuite.addTest(EmployeeTestCase('last_working_period_none_found'))
employeeTestSuite.addTest(EmployeeTestCase('name_properties'))
#employeeTestSuite.addTest(EmployeeTestCase('save'))
