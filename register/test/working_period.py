import unittest2 as unittest
from test_utilities import ModelTestCase, clear_database, \
        get_organization_project_task, get_employee

from datetime import datetime, timedelta

from django.contrib import auth
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

from register.models import Employee, Organization, Task, Project, WorkingPeriod
from settings import NETUNONG_DATE_FORMAT, NETUNONG_TIME_FORMAT

class WorkingPeriodTestCase(ModelTestCase):
    def __init__(self, methodName='runTest'):
        ModelTestCase.__init__(self, methodName)

    def setUp(self):
        (
            self.organization, 
            self.project, 
            self.task
        ) = get_organization_project_task()
        self.employee = get_employee(self.organization)

    def is_complete(self):
        wp1 = WorkingPeriod(employee=self.employee,
                intended="test if employee has working period",
                intended_task=self.task,
                executed="made the employe have it",
                executed_task=self.task,
                start= datetime.now(), end=datetime.now())
        self.assertTrue(wp1.is_complete())
        wp2 = WorkingPeriod(intended_task=self.task,
                employee=self.employee,
                intended="test if employee has working period again",
                start= datetime.now())
        self.assertFalse(wp2.is_complete())         

    def last_activity_last_task(self):
        wp1 = WorkingPeriod(employee=self.employee,
                intended="test if employee has working period",
                intended_task=self.task,
                executed="made the employe have it",
                executed_task=self.task,
                start= datetime.now(), end=datetime.now())
        self.assertEqual(wp1.last_activity, wp1.executed)
        self.assertEqual(wp1.last_task, wp1.executed_task)
        wp2 = WorkingPeriod(intended_task=self.task,
                employee=self.employee,
                intended="test if employee has working period again",
                start= datetime.now())
        self.assertEqual(wp2.last_activity, wp2.intended)
        self.assertEqual(wp2.last_task, wp2.intended_task)

    def last_activity_without_end(self):
        task1 = self.task
        task2 = Task(name="Another task", project=self.project, 
            description="Just another task")
        wp1 = WorkingPeriod(employee=self.employee,
                intended="test if employee has working period",
                intended_task=task1,
                executed="made the employe have it",
                executed_task=task2,
                start= datetime.now(), end=datetime.now())
        self.assertEqual(wp1.last_activity, wp1.executed)
        self.assertEqual(wp1.last_task, wp1.executed_task)
        wp2 = WorkingPeriod(intended_task=task2,
                employee=self.employee,
                intended="test if employee has working period again",
                executed="i tested it", executed_task=task1,
                start= datetime.now())
        self.assertEqual(wp2.last_activity, wp2.executed)
        self.assertEqual(wp2.last_task, wp2.executed_task)

    def total_time(self):
        wp1 = WorkingPeriod(employee=self.employee,
                intended="test if employee has working period",
                intended_task=self.task,
                executed="made the employe have it",
                executed_task=self.task,
                start=datetime(2011, 1, 23, 1, 8), 
                end=  datetime(2011, 1, 23, 9, 38))
        self.assertEqual(wp1.total_time, 8.5)
        self.assertEqual(wp1.timedelta, timedelta(0, (9-1)*60*60 + (38-8)*60))
        self.assertEqual(wp1.hours_minutes, (8, 30))
        self.assertEqual(wp1.hours, 8)
        self.assertEqual(wp1.minutes, 30)
        
        wp2 = WorkingPeriod(intended_task=self.task,
                employee=self.employee,
                intended="test if employee has working period again",
                start=datetime(2011, 1, 23, 1, 8))
        self.assertEqual(wp2.total_time, None)
        self.assertEqual(wp2.timedelta, None)
        self.assertEqual(wp2.hours_minutes, None)
        self.assertEqual(wp2.hours, None)
        self.assertEqual(wp2.minutes, None)

    def save_without_intended_task(self):
        wp1 = WorkingPeriod(employee=self.employee,
                intended="test if employee has working period",
                #intended_task=self.task, # no task
                start= datetime.now())
        wp1.save()

    def formatted_time_values(self):
        wp1 = WorkingPeriod(employee=self.employee,
                intended="test if employee has working period",
                intended_task=self.task,
                executed="made the employe have it",
                executed_task=self.task,
                start=datetime(2011, 1, 23, 1, 8), 
                end=  datetime(2011, 1, 23, 9, 38))
        self.assertEqual(wp1.formatted_start_date, 
                wp1.start.strftime(NETUNONG_DATE_FORMAT))
        self.assertEqual(wp1.formatted_start_time, 
                wp1.start.strftime(NETUNONG_TIME_FORMAT))
        self.assertEqual(wp1.formatted_end_date, 
                wp1.end.strftime(NETUNONG_DATE_FORMAT))
        self.assertEqual(wp1.formatted_end_time, 
                wp1.end.strftime(NETUNONG_TIME_FORMAT))

        wp2 = WorkingPeriod(intended_task=self.task,
                employee=self.employee,
                intended="test if employee has working period again",
                start=datetime(2011, 1, 23, 1, 8))
        self.assertEqual(wp2.formatted_end_date, '')
        self.assertEqual(wp2.formatted_end_time, '')
        
    def tearDown(self):
        clear_database()

workingPeriodTestSuite = unittest.TestSuite()
workingPeriodTestSuite.addTest(WorkingPeriodTestCase('is_complete'))
workingPeriodTestSuite.addTest(WorkingPeriodTestCase('save_without_intended_task'))
workingPeriodTestSuite.addTest(WorkingPeriodTestCase('last_activity_last_task'))
workingPeriodTestSuite.addTest(WorkingPeriodTestCase('last_activity_without_end'))
workingPeriodTestSuite.addTest(WorkingPeriodTestCase('total_time'))
workingPeriodTestSuite.addTest(WorkingPeriodTestCase('save_without_intended_task'))
workingPeriodTestSuite.addTest(WorkingPeriodTestCase('formatted_time_values'))
