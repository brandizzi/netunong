import unittest2 as unittest

from register.models import Task, Project, Employee, Organization, WorkingPeriod
from django.contrib.auth.models import User

class ModelTestCase(unittest.TestCase):

    def __init__(self, methodName='runTest'):
        unittest.TestCase.__init__(self, methodName)

    def clearDatabase(self):
        for model in Task, Project, User, Employee, Organization:
            for instance in model.objects.all():
                instance.delete()
