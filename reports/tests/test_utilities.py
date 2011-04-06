import unittest2 as unittest
from datetime import datetime

from register.tests.test_utilities import ModelTestCase, clear_database, \
        get_employee, get_organization_project_task

from register.models import WorkingPeriod
from reports.models import Contract

class ContractModelTestCase(ModelTestCase):

    def get_working_periods(self, only_april=True):
        organization, project, task = get_organization_project_task(
            organization=self.employee.organization)

        contract = Contract(employee=self.employee, workload=8)
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
        if not only_april:
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
                 ] + wps + [
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
        return wps

