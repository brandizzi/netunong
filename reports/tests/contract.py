from datetime import datetime
import unittest2 as unittest

from register.tests.test_utilities import clear_database, \
        get_employee, get_organization_project_task
from reports.tests.test_utilities import ContractModelTestCase

from register.models import WorkingPeriod
from reports.models import Contract

class ContractTestCase(ContractModelTestCase):

    def __init__(self, methodName):
        ContractModelTestCase.__init__(self, methodName)

    def setUp(self):
        self.employee = get_employee()
        self.contract = Contract(employee=self.employee, workload=8)

    def time_worked(self):
        organization, project, task = get_organization_project_task()
        wps = self.get_working_periods()
        
        start=datetime(2011, 4, 1)
        end=datetime(2011, 4, 30)
        
        time_worked = self.contract.time_worked(start, end)
        self.assertEqual(time_worked, 8-4 + 18-14 + 8-4 + 18-13)

    def time_worked_ignore_those_out_the_interval(self):
        organization, project, task = get_organization_project_task()
        wps = self.get_working_periods(only_april=False)
        for wp in wps: wp.save()
        
        start=datetime(2011, 4, 1)
        end=datetime(2011, 4, 30)
        
        time_worked = self.contract.time_worked(start, end)
        self.assertEqual(time_worked, 8-4 + 18-14 + 8-4 + 18-13)

    def due_payment(self):
        organization, project, task = get_organization_project_task()
        start=datetime(2011, 4, 1)
        end=datetime(2011, 4, 30)
        
        with self.assertRaises(NotImplementedError):
            due_payment = self.contract.due_payment(start, end)
            

    def tearDown(self):
        self.employee.delete_with_user()        

contractTestSuite = unittest.TestSuite()
contractTestSuite.addTest(ContractTestCase('time_worked'))
contractTestSuite.addTest(ContractTestCase('time_worked_ignore_those_out_the_interval'))
contractTestSuite.addTest(ContractTestCase('due_payment'))


