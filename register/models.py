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

        >>> organization = Organization(name="SEA", description="SEA Tecnologia")
        >>> organization.save()
        >>> employee = Employee.create_employee(organization=organization,
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
        >>> employee.user.delete()
        >>> employee.organization.delete()
        >>> employee.delete()
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

        >>> organization = Organization(name="SEA", description="SEA Tecnologia")
        >>> organization.save()
        >>> employee = Employee.create_employee(organization=organization,
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
        >>> organization.delete()
        """
        self.user.delete()
        models.Model.delete(self)

    def get_last_working_period(self):
        return self.workingperiod_set.latest()

class WorkingPeriod(models.Model):
    employee = models.ForeignKey(Employee)
    activity = models.CharField(max_length=500)
    task = models.ForeignKey(Task)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True)

    def __cmp__(self, other):
        """Required for using TestCase.assertItemsEqual()"""
        return self.id - other.id

    class Meta:
        get_latest_by = "start"
