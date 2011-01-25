import unittest2 as unittest
from test_utilities import ModelTestCase, get_organization_project, get_employee

from register.models import Employee, Organization, Task, Project, WorkingPeriod
from django.contrib import auth
from django.contrib.auth.models import User

class TaskTestCase(ModelTestCase):

    def __init__(self, methodName='runTest'):
        ModelTestCase.__init__(self, methodName)

    def setUp(self):
        self.organization, self.project = get_organization_project()
        self.employee = get_employee(self.organization)

taskTestSuite = unittest.TestSuite()
