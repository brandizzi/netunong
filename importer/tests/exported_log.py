import os.path
from datetime import datetime


from register.models import WorkingPeriod
from register.tests.test_utilities import \
        get_organization_project_task, get_employee

from importer.models import ExportedLog
from importer.tests.util import ModelTestCase

class ExportedLogTestCase(ModelTestCase):

    def test_is_exported(self):
        org, _, task = get_organization_project_task()
        emp = get_employee(org)
        start = datetime(2011, 12, 31, 8, 0)
        end = datetime(2011, 12, 31, 12, 0)
        wp = WorkingPeriod(employee=emp,
            intended="Write a function for creating better descriptions",
            intended_task=task,
            executed="Created function to describe exported WP",
            executed_task=task,
            start= start, end=end)
        wp.save()
        self.assertFalse(ExportedLog.is_exported(wp))
        el = ExportedLog(working_period=wp)
        el.save()
        self.assertTrue(ExportedLog.is_exported(wp))
        
        
