from datetime import datetime
import unittest2 as unittest

from register.tests.test_utilities import clear_database, \
        get_employee, get_organization_project_task
from reports.tests.test_utilities import ContractModelTestCase

from register.models import WorkingPeriod
from reports.models import Contract, PJContract

class PJContractTestCase(ContractModelTestCase):

    def __init__(self, methodName):
        ContractModelTestCase.__init__(self, methodName)

    def setUp(self):
        self.employee = get_employee()
        self.contract = PJContract(employee=self.employee, workload=8, hour_value=15)
        self.contract.save()

    def created_contract(self):
        contract = PJContract.objects.get(employee=self.employee)
        self.assertEqual(self.contract, contract)

    def time_worked(self):
        organization, project, task = get_organization_project_task()
        wps = self.get_working_periods()
        
        start=datetime(2011, 4, 1)
        end=datetime(2011, 4, 30)
        
        time_worked = self.contract.time_worked(start, end)
        self.assertEqual(time_worked, 8-4 + 18-14 + 8-4 + 18-13)

    def due_payment(self):
        organization, project, task = get_organization_project_task()
        wps = self.get_working_periods(only_april=False)
        
        start=datetime(2011, 4, 1)
        end=datetime(2011, 4, 30)

        # Time worked should work as in Contract
        time_worked = self.contract.time_worked(start, end)
        self.assertEqual(time_worked, 8-4 + 18-14 + 8-4 + 18-13)
        # NOW THE INTERESTING PART!
        # Payment should be the number of hours times the hour value:
        self.assertEqual(self.contract.due_payment(start, end), 
                time_worked*self.contract.hour_value)
        
    def tearDown(self):
        self.contract.delete()
        self.employee.delete_with_user()    

pjContractTestSuite = unittest.TestSuite()
pjContractTestSuite.addTest(PJContractTestCase('created_contract'))
pjContractTestSuite.addTest(PJContractTestCase('due_payment'))


