from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.contrib import auth

class Organization(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    organization = models.ForeignKey(Organization)

class Task(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    project = models.ForeignKey(Project)

    def __str__(self):
        return "Task(name=%s)" % self.name

    def __cmp__(self, other):
        """Required for using TestCase.assertItemsEqual()"""
        return self.id - other.id

class Employee(models.Model):
    middle_name = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    organization = models.ForeignKey(Organization)
    tasks = models.ManyToManyField(Task, null=True)

    @staticmethod
    def create_employee(organization, username, password, first_name=None, middle_name=None, 
            last_name=None, email=None):
        """
        Creates a new employee and a correspondent user. If we do:

        >>> import test.test_utilities as tu
        >>> org = tu.get_organization()
        >>> employee = Employee.create_employee(organization=org,
        ...     username="test", first_name="Test", last_name="Testein",
        ...     middle_name="Testos", email="test@test.tst", password="test")

        we will have an emnployee in the database:

        >>> employee = Employee.objects.get(middle_name="Testos")
        >>> employee is not None
        True

        and also an user:

        >>> user = auth.authenticate(username='test', password='test')
        >>> user is not None
        True
        >>> user.first_name == "Test"
        True
        >>> user.last_name == "Testein"
        True
        >>> user.email == "test@test.tst"
        True

        who will be associated to the employee:

        >>> employee.user == user
        True

        Cleanup:
        >>> tu.clear_database()
        """
        user = User.objects.create_user(username=username, password=password,
                email=email)
        user.first_name=first_name
        user.last_name=last_name
        user.save()

        employee = Employee(user=user, middle_name=middle_name, 
            organization=organization)
        employee.save()
        return employee

    def delete_with_user(self):
        """
        Deletes an employee and its user. If we create an employee:

        >>> import test.test_utilities as tu
        >>> org = tu.get_organization()
        >>> employee = Employee.create_employee(organization=org,
        ...     username="test", first_name="Test", last_name="Testein",
        ...     middle_name="Testos", email="test@test.tst", password="test")

        and it is in the database:

        >>> employee = Employee.objects.get(middle_name="Testos")
        >>> employee is not None
        True

        as well as its user:

        >>> user = User.objects.get(username='test')
        >>> user is not None
        True
        >>> employee.user == user
        True

        and we call this method:

        >>> employee.delete_with_user()

        both the employer and the user are removed from de database:

        >>> Employee.objects.all()
        []
        >>> User.objects.all()
        []

        Cleanup:
        >>> tu.clear_database()
        """
        self.user.delete()
        models.Model.delete(self)

    def get_last_working_period(self):
        """
        Get the last working period, ordered by the moment it started.

        >>> import test.test_utilities as tu
        >>> org, _, task = tu.get_organization_project_task()
        >>> employee = tu.get_employee(org)
        >>> wp1 = WorkingPeriod( employee=employee,
        ...     intended="test if employee has working period", intended_task=task, 
        ...     executed="I've done it!", executed_task=task, 
        ...     start= datetime.now(), end=datetime.now())
        >>> wp2 = WorkingPeriod(intended_task=task, employee=employee,
        ...     intended="test if employee has working period again",
        ...     start= datetime.now())
        >>> wp1.save()
        >>> wp2.save()
        >>> employee.get_last_working_period() == wp2
        True

        Cleanup:
        >>> tu.clear_database()
        """
        try:
            return self.workingperiod_set.latest()
        except WorkingPeriod.DoesNotExist:
            return WorkingPeriod.NONE

class WorkingPeriod(models.Model):
    employee = models.ForeignKey(Employee)

    start = models.DateTimeField()
    intended = models.CharField(max_length=200)
    intended_task = models.ForeignKey(Task, 
            related_name='intended_working_periods')

    end = models.DateTimeField(null=True)
    executed = models.CharField(max_length=200, null=True)
    executed_task = models.ForeignKey(Task, null=True, 
            related_name='executed_working_periods')

    def is_complete(self):
        """
        Returns True if the period is complete --- that is, its end field is
        filled; returns False otherwise.

        >>> import test.test_utilities as tu
        >>> org, _, task = tu.get_organization_project_task()
        >>> employee = tu.get_employee(org)
        >>> wp1 = WorkingPeriod(employee=employee,
        ...     intended="test if employee has working period", intended_task=task, 
        ...     executed="made the employe have it", executed_task=task, 
        ...     start= datetime.now(), end=datetime.now())
        >>> wp1.save()
        >>> wp1.is_complete()
        True
        >>> wp2 = WorkingPeriod(intended_task=task, employee=employee,
        ...     intended="test if employee has working period again",
        ...     start= datetime.now())
        >>> wp2.save()
        >>> wp2.is_complete()
        False

        Cleanup:
        >>> tu.clear_database()
        """
        return self.end is not None

    def __cmp__(self, other):
        """Required for using TestCase.assertItemsEqual()"""
        return self.id - other.id

    class Meta:
        get_latest_by = "start"

# Represents the null working period. Better than verifying if the working
# period is None
WorkingPeriod.NONE = WorkingPeriod()
WorkingPeriod.NONE.is_complete = lambda : True
