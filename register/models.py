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

class WorkingPeriod(models.Model):
    activity = models.CharField(max_length=500)
    task = models.ForeignKey(Task)
    start = models.TimeField()
    end = models.TimeField()

class Employee(models.Model):
    user = models.ForeignKey(User)
    middle_name = models.CharField(max_length=200)

    @staticmethod
    def create_employee(username, password, first_name=None, middle_name=None, 
            last_name=None, email=None):
        """
        Creates a new employee and a correspondent user. If we do:

        >>> employee = Employee.create_employee(
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
        >>> employee.delete()
        """
        user = User.objects.create_user(username=username, password=password,
                email=email)
        user.first_name=first_name
        user.last_name=last_name
        user.save()

        employee = Employee(user=user, middle_name=middle_name)
        employee.save()
        return employee

    def delete_with_user(self):
        """
        Deletes an employee and its user. If we create an employee:

        >>> employee = Employee.create_employee(
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
        """
        self.user.delete()
        models.Model.delete(self)
