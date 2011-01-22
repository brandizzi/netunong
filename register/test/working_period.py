import unittest2 as unittest
from test_utilities import ModelTestCase, clear_database, \
        get_organization_project_task, get_employee

from datetime import datetime

from register.models import Employee, Organization, Task, Project, WorkingPeriod
from django.contrib import auth
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

class WorkingPeriodTestCase(ModelTestCase):
    def __init__(self, methodName='runTest'):
        ModelTestCase.__init__(self, methodName)

    def setUp(self):
        (self.organization, self.project, 
                self.task) = get_organization_project_task()
        self.employee = get_employee(self.organization)

    def is_complete(self):
        wp1 = WorkingPeriod(employee=self.employee,
                intended="test if employee has working period",
                intended_task=self.task,
                executed="made the employe have it",
                executed_task=self.task,
                start= datetime.now(), end=datetime.now())
        wp1.save()
        self.assertTrue(wp1.is_complete())
        wp2 = WorkingPeriod(intended_task=self.task,
                employee=self.employee,
                intended="test if employee has working period again",
                start= datetime.now())
        wp2.save()
        self.assertFalse(wp2.is_complete())         

    def save_without_intended_task(self):
        wp1 = WorkingPeriod(employee=self.employee,
                intended="test if employee has working period",
                #intended_task=self.task, # no task
                start= datetime.now())
        wp1.save()

    def tearDown(self):
        clear_database()

workingPeriodTestSuite = unittest.TestSuite()
workingPeriodTestSuite.addTest(WorkingPeriodTestCase('is_complete'))
workingPeriodTestSuite.addTest(WorkingPeriodTestCase('save_without_intended_task'))
