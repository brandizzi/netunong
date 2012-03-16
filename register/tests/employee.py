from test_utilities import ModelTestCase, clear_database

from datetime import datetime, time, timedelta

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


    def test_create_employee(self):
        employee = self.get_default_employee()

        user = auth.authenticate(username='test', password='test')
        self.assertIsNotNone(user, "User should be created")

        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "Testein")
        self.assertEqual(user.email, "test@test.tst")

        employee = Employee.objects.get(user=user)
        self.assertIsNotNone(employee, "Employee should be found")
        self.assertEqual(employee.middle_name, "Testos")

    def test_detele_with_user(self):
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

    def test_reject_repeated_username(self):
        employee = self.get_default_employee()
        with self.assertRaises(Exception):
            employee = Employee.create_employee(organization=self.organization,
                    username="test", first_name="Test", last_name="Testein",
                    middle_name="Testos", email="test@test.tst", 
                    password="test")

    def test_has_organization(self):
        organization = Organization(name="SEA Tecnologia",
                description="Criadora do Netuno Nova Geracao (NetunoNG)")
        organization.save()
        employee = Employee.create_employee(organization=organization,
                username="test", first_name="Test", last_name="Testein",
                middle_name="Testos", email="test@test.tst", password="test")

        self.assertEqual(employee.organization, organization)
        retrieved = Employee.objects.get(middle_name='Testos')
        self.assertEqual(retrieved.organization, organization)
        
    def test_has_tasks(self):
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

    def test_has_working_periods(self):
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

    def test_last_working_period(self):
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

    def test_order_working_periods_by_start_date(self):
        employee = self.get_default_employee()

        project = Project(name="Project 1", description="First project",
                    organization=self.organization)
        project.save()
        task = Task(name="Test employee", project=project, 
                description="Testing the Employee model")
        task.save()

        now = datetime.now()
        past = now-timedelta(1)
        future = now+timedelta(1)

        now_wp = WorkingPeriod(employee=employee,
                intended="Be now",
                intended_task=task,
                executed="Be now",
                executed_task=task,
                start= now, end=now)
        past_wp = WorkingPeriod(employee=employee,
                intended="Be in past",
                intended_task=task,
                executed="Be in past",
                executed_task=task,
                start=past, end=past)
        future_wp = WorkingPeriod(employee=employee,
                intended="Be in futore",
                intended_task=task,
                executed="Be in future",
                executed_task=task,
                start=future, end=future)

        now_wp.save()
        past_wp.save()
        future_wp.save()

        self.assertEquals(employee.workingperiod_set.all()[0], past_wp)
        self.assertEquals(employee.workingperiod_set.all()[1], now_wp)
        self.assertEquals(employee.workingperiod_set.all()[2], future_wp)

    def test_order_working_periods_by_end_date(self):
        employee = self.get_default_employee()

        project = Project(name="Project 1", description="First project",
                    organization=self.organization)
        project.save()
        task = Task(name="Test employee", project=project, 
                description="Testing the Employee model")
        task.save()

        now = datetime.now()
        past = now-timedelta(1)
        future = now+timedelta(1)

        now_wp = WorkingPeriod(employee=employee,
                intended="Be now",
                intended_task=task,
                executed="Be now",
                executed_task=task,
                start= past, end=now)
        past_wp = WorkingPeriod(employee=employee,
                intended="Be in past",
                intended_task=task,
                executed="Be in past",
                executed_task=task,
                start=past, end=past)
        future_wp = WorkingPeriod(employee=employee,
                intended="Be in futore",
                intended_task=task,
                executed="Be in future",
                executed_task=task,
                start=past, end=future)

        now_wp.save()
        past_wp.save()
        future_wp.save()

        self.assertEquals(employee.workingperiod_set.all()[0], past_wp)
        self.assertEquals(employee.workingperiod_set.all()[1], now_wp)
        self.assertEquals(employee.workingperiod_set.all()[2], future_wp)

    def test_last_working_period_none_found(self):
        employee = self.get_default_employee()

        project = Project(name="Project 1", description="First project",
                    organization=self.organization)
        project.save()
        task = Task(name="Test employee", project=project, 
                description="Testing the Employee model")
        task.save()

        self.assertIs(employee.last_working_period, WorkingPeriod.NONE)
        
    def test_name_properties(self):
        employee = self.get_default_employee()
        self.assertEqual(employee.first_name, employee.user.first_name)
        self.assertEqual(employee.last_name, employee.user.last_name)
        self.assertEqual(employee.name, "%s %s %s" % ( 
                    employee.first_name, employee.middle_name, employee.last_name
             ))


    def test_get_only_not_done_tasks(self):
        employee = self.get_default_employee()
        project = Project(name="Project 1", description="First project",
            organization=self.organization)
        done_task = Task(project=project, description='task', name='is done')
        done_task.save()
        not_done_task = Task(project=project, description='task', 
                name='Not done')
        not_done_task.save()

        employee.tasks.add(done_task, not_done_task)

        employee = Employee.objects.get(id=employee.id)
        self.assertItemsEqual([not_done_task, done_task], 
                employee.not_done_tasks)

        done_task.done = True
        done_task.save()

        self.assertItemsEqual([not_done_task], employee.not_done_tasks)

        
    def get_default_employee(self):
        return Employee.create_employee(organization=self.organization,
                username="test", first_name="Test", last_name="Testein",
                middle_name="Testos", email="test@test.tst", password="test")

    def tearDown(self):
        clear_database()

