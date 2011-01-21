import unittest2 as unittest
from test_utilities import ModelTestCase

from register.models import Employee, Organization, Task, Project, WorkingPeriod
from django.contrib import auth
from django.contrib.auth.models import User

class TaskTestCase(ModelTestCase):

    def __init__(self, methodName='runTest'):
        ModelTestCase.__init__(self, methodName)

    def setUp(self):
        self.organization = Organization(name="SEA Tecnologia",
                description="Criadora do Netuno Nova Geracao (NetunoNG)")
        self.organization.save()

        self.project = Project(organization=self.organization, name="Netuno NG", 
                description="Netuno Nova Geracao (NetunoNG)"
        self.project.save()

#    def get_last_working_period(self):
#        task = Task(name="Test Tasks", project=self.project, 
#                description="Writing tests for task models")

#        wp1 = WorkingPeriod(task=task, 
#                activity="Testing get_last_working_period"

#         activity = models.CharField(max_length=500)
#    task = models.ForeignKey(Task)
#    start = models.TimeField()
#    end = models.TimeField()
