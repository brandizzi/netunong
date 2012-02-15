import threading
import time
from datetime import datetime

import mechanize

from importer.models import ImportedEntity
from importer.parser import get_exported_description
from register.models import Task, WorkingPeriod
import importer.agent as agents

from register.tests.test_utilities import \
        get_organization, get_employee

from importer.tests.util import NetunomockTestCase, ModelTestCase

from netunomock.server import ROOT_URL, SHOW_LOGS_PATH

class ExporterTestCase(NetunomockTestCase, ModelTestCase):

    def test_export(self): 
        emp = get_employee(get_organization())    
        agents.importer.import_all(ROOT_URL, 'adam', 'senha')

        e = ImportedEntity.objects.get(category='T', original_id=2376)
        task = Task.objects.get(id=e.new_id)
        start = datetime(2011, 12, 31, 8, 0)
        end = datetime(2011, 12, 31, 12, 0)

        wp = WorkingPeriod(employee=emp,
            intended="Write a function for creating better descriptions",
            intended_task=task,
            executed="Created function to describe exported WP",
            executed_task=task,
            start= start, end=end)
        wp.save()

        exporter = agents.Exporter()
        exporter.export_logs([wp], ROOT_URL, 'adam', 'senha')
        
        browser = mechanize.Browser()
        response = browser.open(ROOT_URL + SHOW_LOGS_PATH)
        content = response.read().decode('utf-8')
        self.assertTrue(('Task id: 2376') in content)
        self.assertTrue('Log creator: 1' in content)
        self.assertTrue(('Date: %s' % start.strftime("%Y%m%d")) in content)
        self.assertTrue('Worked hours: %s' % wp.hours in content)
        self.assertTrue('Description: %s' % get_exported_description(wp) in content)
        

    def setUp(self):
        NetunomockTestCase.setUp(self)
        ModelTestCase.setUp(self)
        
    def tearDown(self):
        NetunomockTestCase.tearDown(self)
        ModelTestCase.tearDown(self)
