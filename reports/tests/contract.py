from datetime import datetime
import unittest2 as unittest

from register.tests.test_utilities import ModelTestCase, clear_database, \
        get_employee, get_organization_project_task

from register.models import WorkingPeriod
from reports.models import Contract

class ContractTestCase(ModelTestCase):

    def __init__(self, methodName):
        ModelTestCase.__init__(self, methodName)

    def setUp(self):
        self.employee = get_employee()

    def create_contract(self):
        contract = Contract(employee=self.employee, workload=8, salary=2000)

    def time_worked(self):
        organization, project, task = get_organization_project_task()

        contract = Contract(employee=self.employee, workload=8, salary=2000)
        #contract.save()

        wps = [
            WorkingPeriod(employee=self.employee,
                executed="made the employe have it",
                executed_task=task,
                start=datetime(2011, 4, 4, 8, 0, 0),
                end=datetime(2011, 4, 4, 12, 0, 0)),
            WorkingPeriod(employee=self.employee,
                executed="test if employee has working period again",
                executed_task=task,
                start=datetime(2011, 4, 4, 14, 0, 0),
                end=datetime(2011, 4, 4, 18, 0, 0)),
            WorkingPeriod(employee=self.employee,
                executed="made the employe have it",
                executed_task=task,
                start=datetime(2011, 4, 5, 8, 0, 0),
                end=datetime(2011, 4, 5, 12, 0, 0)),
            WorkingPeriod(employee=self.employee,
                executed="made the employe have it",
                executed_task=task,
                start=datetime(2011, 4, 5, 13, 0, 0),
                end=datetime(2011, 4, 5, 18, 0, 0)),
        ]
        for wp in wps: wp.save()
        
        start=datetime(2011, 4, 1)
        end=datetime(2011, 4, 30)
        
        time_worked = contract.time_worked(start, end)
        self.assertEqual(time_worked, 8-4 + 18-14 + 8-4 + 18-13)

    def time_worked_ignore_those_out_the_interval(self):
        organization, project, task = get_organization_project_task()

        contract = Contract(employee=self.employee, workload=8, salary=2000)

        wps = [
            # Out the interval
            WorkingPeriod(employee=self.employee,
                executed="made the employe have it",
                executed_task=task,
                start=datetime(2011, 3, 31, 8, 0, 0),
                end=datetime(2011, 3, 31, 12, 0, 0)),
            WorkingPeriod(employee=self.employee,
                executed="test if employee has working period again",
                executed_task=task,
                start=datetime(2011, 3, 31, 14, 0, 0),
                end=datetime(2011, 3, 31, 18, 0, 0)),
            # in the interval
            WorkingPeriod(employee=self.employee,
                executed="made the employe have it",
                executed_task=task,
                start=datetime(2011, 4, 4, 8, 0, 0),
                end=datetime(2011, 4, 4, 12, 0, 0)),
            WorkingPeriod(employee=self.employee,
                executed="test if employee has working period again",
                executed_task=task,
                start=datetime(2011, 4, 4, 14, 0, 0),
                end=datetime(2011, 4, 4, 18, 0, 0)),
            WorkingPeriod(employee=self.employee,
                executed="made the employe have it",
                executed_task=task,
                start=datetime(2011, 4, 5, 8, 0, 0),
                end=datetime(2011, 4, 5, 12, 0, 0)),
            WorkingPeriod(employee=self.employee,
                executed="made the employe have it",
                executed_task=task,
                start=datetime(2011, 4, 5, 13, 0, 0),
                end=datetime(2011, 4, 5, 18, 0, 0)),
            #out the interval
            WorkingPeriod(employee=self.employee,
                executed="made the employe have it",
                executed_task=task,
                start=datetime(2011, 5, 1, 8, 0, 0),
                end=datetime(2011, 5, 1, 12, 0, 0)),
            WorkingPeriod(employee=self.employee,
                executed="test if employee has working period again",
                executed_task=task,
                start=datetime(2011, 5, 1, 14, 0, 0),
                end=datetime(2011, 5, 1, 18, 0, 0)),
        ]
        for wp in wps: wp.save()
        
        start=datetime(2011, 4, 1)
        end=datetime(2011, 4, 30)
        
        time_worked = contract.time_worked(start, end)
        self.assertEqual(time_worked, 8-4 + 18-14 + 8-4 + 18-13)

    def tearDown(self):
        self.employee.delete_with_user()        

contractTestSuite = unittest.TestSuite()
contractTestSuite.addTest(ContractTestCase('create_contract'))
contractTestSuite.addTest(ContractTestCase('time_worked'))
contractTestSuite.addTest(ContractTestCase('time_worked_ignore_those_out_the_interval'))


