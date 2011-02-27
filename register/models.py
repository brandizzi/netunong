from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import admin
from settings import NETUNONG_DATE_FORMAT, NETUNONG_TIME_FORMAT



class Organization(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    class Admin:
        pass

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    organization = models.ForeignKey(Organization)

    class Admin:
        pass

class Task(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    project = models.ForeignKey(Project)

    def __str__(self):
        return "Task(name=%s)" % self.name

    def __cmp__(self, other):
        """Required for using TestCase.assertItemsEqual()"""
        return self.id - other.id

    class Admin:
        pass

class Employee(models.Model):
    middle_name = models.CharField(max_length=200)
    user = models.OneToOneField(User)
    organization = models.ForeignKey(Organization)
    tasks = models.ManyToManyField(Task, null=True)

    @staticmethod
    def create_employee(organization, username, password, first_name=None, middle_name=None, 
            last_name=None, email=None):
        """
        Creates a new employee and a correspondent user. If we do:

        >>> import tests.test_utilities as tu
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

        >>> import tests.test_utilities as tu
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

        both the employee and the user are removed from de database:

        >>> Employee.objects.all()
        []
        >>> User.objects.all()
        []

        Cleanup:
        >>> tu.clear_database()
        """
        self.user.delete()
        models.Model.delete(self)

    @property
    def last_working_period(self):
        """
        Get the last working period, ordered by the moment it started.

        >>> import tests.test_utilities as tu
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
        >>> employee.last_working_period == wp2
        True

        Cleanup:
        >>> tu.clear_database()
        """
        try:
            return self.workingperiod_set.latest()
        except WorkingPeriod.DoesNotExist:
            return WorkingPeriod.NONE

    @property
    def first_name(self):
        """
        Returns the first name which is actually stored at the user:

        >>> import tests.test_utilities as tu
        >>> employee = tu.get_employee()
        >>> employee.first_name
        'Test'
        >>> employee.first_name == employee.user.first_name
        True
        >>> tu.clear_database()
        """
        return self.user.first_name

    @property
    def last_name(self):
        """
        Returns the last name which is actually stored at the user:

        >>> import tests.test_utilities as tu
        >>> employee = tu.get_employee()
        >>> employee.last_name
        'Testein'
        >>> employee.first_name == employee.user.first_name
        True
        >>> tu.clear_database()
        """
        return self.user.last_name

    @property
    def name(self):
        """
        Returns the employee's full name:

        >>> import tests.test_utilities as tu
        >>> employee = tu.get_employee()
        >>> employee.name
        'Test Testos Testein'
        >>> tu.clear_database()
        """
        return " ".join([self.first_name, self.middle_name, self.last_name])

    class Admin:
        pass
        
class WorkingPeriod(models.Model):
    employee = models.ForeignKey(Employee)

    start = models.DateTimeField()
    intended = models.CharField(max_length=200)
    intended_task = models.ForeignKey(Task, 
            related_name='intended_working_periods', null=True)

    end = models.DateTimeField(null=True)
    executed = models.CharField(max_length=200, null=True)
    executed_task = models.ForeignKey(Task, null=True, 
            related_name='executed_working_periods')

    def is_complete(self):
        """
        Returns True if the period is complete --- that is, its end field is
        filled; returns False otherwise.

        >>> import tests.test_utilities as tu
        >>> org, _, task = tu.get_organization_project_task()
        >>> employee = tu.get_employee(org)
        >>> wp1 = WorkingPeriod(employee=employee,
        ...     intended="test if employee has working period", intended_task=task, 
        ...     executed="made the employee have it", executed_task=task, 
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

    @property
    def last_activity(self):
        """
        If the working period is complete, return the "executed" field; return
        the "intended" field.
        
        >>> import tests.test_utilities as tu
        >>> org, _, task = tu.get_organization_project_task()
        >>> employee = tu.get_employee(org)
        >>> wp1 = WorkingPeriod(employee=employee,
        ...     intended="test if employee has working period", intended_task=task, 
        ...     executed="made the employee have it", executed_task=task, 
        ...     start= datetime.now(), end=datetime.now())
        >>> wp1.save()
        >>> wp1.last_activity
        'made the employee have it'
        >>> wp2 = WorkingPeriod(intended_task=task, employee=employee,
        ...     intended="test if employee has working period again",
        ...     start= datetime.now())
        >>> wp2.save()
        >>> wp2.last_activity
        'test if employee has working period again'

        Cleanup:
        >>> tu.clear_database()
        """
        return self.executed if self.executed else self.intended
        
    @property
    def last_task(self):
        """
        If the working period is complete, return the executed task; return
        the intended task otherwise.
        
        >>> import tests.test_utilities as tu
        >>> org, _, task = tu.get_organization_project_task()
        >>> employee = tu.get_employee(org)
        >>> wp1 = WorkingPeriod(employee=employee,
        ...     intended="test if employee has working period", intended_task=task, 
        ...     executed="made the employee have it", executed_task=task, 
        ...     start= datetime.now(), end=datetime.now())
        >>> wp1.save()
        >>> wp1.last_task == wp1.executed_task
        True
        >>> wp2 = WorkingPeriod(intended_task=task, employee=employee,
        ...     intended="test if employee has working period again",
        ...     start= datetime.now())
        >>> wp2.save()
        >>> wp2.last_task == wp2.intended_task
        True

        Cleanup:
        >>> tu.clear_database()
        """
        return self.executed_task if self.executed_task else self.intended_task

    @property
    def total_time(self):
        """
        Returns the total time spend in this period, in hours as a float
        (if the period lasted eight hours and thirty minutes, this
        property returns 8.5)
        
        >>> import tests.test_utilities as tu
        >>> org, _, task = tu.get_organization_project_task()
        >>> employee = tu.get_employee(org)
        >>> wp1 = WorkingPeriod(employee=employee,
        ...     intended="test if employee has working period", intended_task=task, 
        ...     executed="made the employee have it", executed_task=task, 
        ...     start=datetime(2011, 1, 23, 1, 8), 
        ...     end=  datetime(2011, 1, 23, 9, 38))
        >>> wp1.total_time
        8.5

        However, it returns the time spent only if both start and end moments
        are still specified for the period. Otherwise it just returns None
        
        >>> wp2 = WorkingPeriod(intended_task=task,
        ...     employee=employee,
        ...     intended="test if employee has working period again",
        ...     start=datetime(2011, 1, 23, 1, 8))
        >>> wp2.total_time == None
        True

        Cleanup:
        >>> tu.clear_database()
        """
        return float(self.timedelta.seconds)/3600 if self.end is not None else None

    @property
    def timedelta(self):
        """
        Returns the timedelta between start and end moments:
        
        >>> import tests.test_utilities as tu
        >>> org, _, task = tu.get_organization_project_task()
        >>> employee = tu.get_employee(org)
        >>> wp1 = WorkingPeriod(employee=employee,
        ...     intended="test if employee has working period", intended_task=task, 
        ...     executed="made the employee have it", executed_task=task, 
        ...     start=datetime(2011, 1, 23, 1, 8), 
        ...     end=  datetime(2011, 1, 23, 9, 38))
        >>> wp1.timedelta
        datetime.timedelta(0, 30600)

        However, it returns the time spent only if both start and end moments
        are still specified for the period. Otherwise it just returns None
        
        >>> wp2 = WorkingPeriod(intended_task=task,
        ...     employee=employee,
        ...     intended="test if employee has working period again",
        ...     start=datetime(2011, 1, 23, 1, 8))
        >>> wp2.timedelta == None
        True

        Cleanup:
        >>> tu.clear_database()
        """
        return self.end - self.start if self.end is not None else None

    @property
    def hours_minutes(self):
        """
        Returs a tuple containing the total of hours spent at the first position
        and the total of minutes which lasted at the second position
        
        >>> import tests.test_utilities as tu
        >>> org, _, task = tu.get_organization_project_task()
        >>> employee = tu.get_employee(org)
        >>> wp1 = WorkingPeriod(employee=employee,
        ...     intended="test if employee has working period", intended_task=task, 
        ...     executed="made the employee have it", executed_task=task, 
        ...     start=datetime(2011, 1, 23, 1, 8), 
        ...     end=  datetime(2011, 1, 23, 9, 38))
        >>> wp1.hours_minutes
        (8, 30)

        However, it returns the tuple only if both start and end moments
        are still specified for the period. Otherwise it just returns None
        
        >>> wp2 = WorkingPeriod(intended_task=task,
        ...     employee=employee,
        ...     intended="test if employee has working period again",
        ...     start=datetime(2011, 1, 23, 1, 8))
        >>> wp2.hours_minutes == None
        True

        Cleanup:
        >>> tu.clear_database()
        """
        if self.timedelta:
            hours, seconds = divmod(self.timedelta.seconds, 3600)
            minutes = seconds/60
            return hours, minutes
        else:
            return None

    @property
    def hours(self):
        """
        Returns the total of hours spent.
        
        >>> import tests.test_utilities as tu
        >>> org, _, task = tu.get_organization_project_task()
        >>> employee = tu.get_employee(org)
        >>> wp1 = WorkingPeriod(employee=employee,
        ...     intended="test if employee has working period", intended_task=task, 
        ...     executed="made the employee have it", executed_task=task, 
        ...     start=datetime(2011, 1, 23, 1, 8), 
        ...     end=  datetime(2011, 1, 23, 9, 38))
        >>> wp1.hours
        8

        However, it returns the hour only if both start and end moments
        are still specified for the period. Otherwise it just returns None
        
        >>> wp2 = WorkingPeriod(intended_task=task,
        ...     employee=employee,
        ...     intended="test if employee has working period again",
        ...     start=datetime(2011, 1, 23, 1, 8))
        >>> wp2.hours == None
        True

        Cleanup:
        >>> tu.clear_database()
        """
        return self.timedelta.seconds/3600 if self.timedelta is not None else None

    @property
    def minutes(self):
        """
        Returns the total of hours spent.
        
        >>> import tests.test_utilities as tu
        >>> org, _, task = tu.get_organization_project_task()
        >>> employee = tu.get_employee(org)
        >>> wp1 = WorkingPeriod(employee=employee,
        ...     intended="test if employee has working period", intended_task=task, 
        ...     executed="made the employee have it", executed_task=task, 
        ...     start=datetime(2011, 1, 23, 1, 8), 
        ...     end=  datetime(2011, 1, 23, 9, 38))
        >>> wp1.minutes
        30

        However, it returns the hour only if both start and end moments
        are still specified for the period. Otherwise it just returns None
        
        >>> wp2 = WorkingPeriod(intended_task=task,
        ...     employee=employee,
        ...     intended="test if employee has working period again",
        ...     start=datetime(2011, 1, 23, 1, 8))
        >>> wp2.minutes == None
        True

        Cleanup:
        >>> tu.clear_database()
        """
        return (self.timedelta.seconds%3600)/60 if self.timedelta is not None else None

    @property
    def formatted_start_date(self):
        """
        Returns a stirng represented the start date according to the 
        NETUNONG_DATE_FORMAT format.
        
        >>> import tests.test_utilities as tu
        >>> org, _, task = tu.get_organization_project_task()
        >>> employee = tu.get_employee(org)
        >>> wp1 = WorkingPeriod(employee=employee,
        ...     intended="test if employee has working period", intended_task=task, 
        ...     executed="made the employee have it", executed_task=task, 
        ...     start=datetime(2011, 1, 23, 1, 8), 
        ...     end=  datetime(2011, 1, 23, 9, 38))
        >>> wp1.formatted_start_date ==  wp1.start.strftime(NETUNONG_DATE_FORMAT)
        True

        Cleanup    
        >>> tu.clear_database()
        """
        return self.start.strftime(NETUNONG_DATE_FORMAT)

    @property
    def formatted_end_date(self):
        """
        Returns a stirng represented the end date according to the 
        NETUNONG_DATE_FORMAT format. THANK YOU DDJANGO FOR MAKING DATE
        READING REALLY DIFFICULT!!
        
        >>> import tests.test_utilities as tu
        >>> org, _, task = tu.get_organization_project_task()
        >>> employee = tu.get_employee(org)
        >>> wp1 = WorkingPeriod(employee=employee,
        ...     intended="test if employee has working period", intended_task=task, 
        ...     executed="made the employee have it", executed_task=task, 
        ...     start=datetime(2011, 1, 23, 1, 8), 
        ...     end=  datetime(2011, 1, 23, 9, 38))
        >>> wp1.formatted_end_date ==  wp1.end.strftime(NETUNONG_DATE_FORMAT)
        True

        Cleanup    
        >>> tu.clear_database()
        """
        return self.end.strftime(NETUNONG_DATE_FORMAT) if self.end else ''

    @property
    def formatted_start_time(self):
        """
        Returns a stirng represented the start time according to the 
        NETUNONG_TIME_FORMAT format.
        
        >>> import tests.test_utilities as tu
        >>> org, _, task = tu.get_organization_project_task()
        >>> employee = tu.get_employee(org)
        >>> wp1 = WorkingPeriod(employee=employee,
        ...     intended="test if employee has working period", intended_task=task, 
        ...     executed="made the employee have it", executed_task=task, 
        ...     start=datetime(2011, 1, 23, 1, 8), 
        ...     end=  datetime(2011, 1, 23, 9, 38))
        >>> wp1.formatted_start_time ==  wp1.start.strftime(NETUNONG_TIME_FORMAT)
        True

        Cleanup    
        >>> tu.clear_database()
        """
        return self.start.strftime(NETUNONG_TIME_FORMAT)

    @property
    def formatted_end_time(self):
        """
        Returns a stirng represented the end date according to the 
        NETUNONG_TIME_FORMAT format.
        
        >>> import tests.test_utilities as tu
        >>> org, _, task = tu.get_organization_project_task()
        >>> employee = tu.get_employee(org)
        >>> wp1 = WorkingPeriod(employee=employee,
        ...     intended="test if employee has working period", intended_task=task, 
        ...     executed="made the employee have it", executed_task=task, 
        ...     start=datetime(2011, 1, 23, 1, 8), 
        ...     end=  datetime(2011, 1, 23, 9, 38))
        >>> wp1.formatted_end_time ==  wp1.end.strftime(NETUNONG_TIME_FORMAT)
        True

        Cleanup    
        >>> tu.clear_database()
        """
        return self.end.strftime(NETUNONG_TIME_FORMAT) if self.end else ''

    def __cmp__(self, other):
        """Required for using TestCase.assertItemsEqual()"""
        return self.id - other.id

    class Meta:
        get_latest_by = "id"


# Represents the null working period. Better than verifying if the working
# period is None
WorkingPeriod.NONE = WorkingPeriod()
WorkingPeriod.NONE.is_complete = lambda : True

admin.autodiscover()
