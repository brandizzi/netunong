import unittest2 as unittest
from test_utilities import ModelTestCase, get_organization_project_task, \
        get_employee

from register.models import  Organization, Task, Project
from django.contrib import auth
from django.contrib.auth.models import User

class TaskTestCase(ModelTestCase):

    def __init__(self, methodName='runTest'):
        ModelTestCase.__init__(self, methodName)

    def setUp(self):
        (
            self.organization, 
            self.project,
            self.task
        ) = get_organization_project_task()
        self.employee = get_employee(self.organization)

    def is_doable(self):
        self.assertFalse(self.task.done)
        self.task.mark_as_done()
        self.assertTrue(self.task.done)

    def save_done_status(self):
        self.assertFalse(self.task.done)
        self.task.mark_as_done()
        self.assertTrue(self.task.done)

        task = Task.objects.get(id=self.task.id)
        self.assertFalse(task.done)
        self.task.mark_as_done()
        self.task.save()

        task = Task.objects.get(id=self.task.id)
        self.assertTrue(task.done)

taskTestSuite = unittest.TestSuite()
taskTestSuite.addTest(TaskTestCase('is_doable'))
taskTestSuite.addTest(TaskTestCase('save_done_status'))
