from datetime import datetime
import unittest2 as unittest

from register.tests.test_utilities import ModelTestCase, clear_database, \
        get_employee, get_organization_project_task

from register.models import WorkingPeriod
from reports.models import Contract, PJContract

class PJContractTestCase(ModelTestCase):

    def __init__(self, methodName):
        ModelTestCase.__init__(self, methodName)

    def setUp(self):
        self.employee = get_employee()

    def create_contract(self):
        contract = PJContract(employee=self.employee, workload=8, hour_value=15)
        contract.save()

        contract2 = PJContract.objects.get(employee=self.employee)
        self.assertEqual(contract, contract2)

    def time_worked(self):
        organization, project, task = get_organization_project_task()

        contract = PJContract(employee=self.employee, workload=8)
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

        contract.delete()

    def due_payment(self):
        organization, project, task = get_organization_project_task()

        contract = PJContract(employee=self.employee, workload=8, hour_value=15)
        contract.save()

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

        # Time worked should work as in Contract
        time_worked = contract.time_worked(start, end)
        self.assertEqual(time_worked, 8-4 + 18-14 + 8-4 + 18-13)
        # NOW THE INTERESTING PART!
        # Payment should be the number of hours times the hour value:
        self.assertEqual(contract.due_payment(start, end), time_worked*contract.hour_value)

        contract.delete()
        
    def tearDown(self):
        self.employee.delete_with_user()        

pjContractTestSuite = unittest.TestSuite()
pjContractTestSuite.addTest(PJContractTestCase('create_contract'))
pjContractTestSuite.addTest(PJContractTestCase('due_payment'))


