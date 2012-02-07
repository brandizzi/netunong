import os.path
from datetime import datetime

import settings

from register.models import WorkingPeriod
from register.tests.test_utilities import \
        get_organization_project_task, get_employee

import importer.models as ExportedLog
from importer.tests.util import ParserTestCase

class ExportedLogTestCase(ParserTestCase):

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
        
        
