import threading
import time
from datetime import datetime, timedelta

import mechanize

from importer.models import ImportedEntity, ExportedLog
from importer.parser import get_exported_description
from register.models import Task, WorkingPeriod
import importer.agent as agents

from register.tests.test_utilities import \
        get_organization, get_employee

from importer.tests.util import NetunomockTestCase, ModelTestCase

from netunomock.server import ROOT_URL, SHOW_LOGS_PATH

class ExporterTestCase(NetunomockTestCase, ModelTestCase):

    def test_export(self): 
        emp, task, start, end = self.get_depencencies()

        wp = WorkingPeriod(employee=emp,
            intended="Write a function for creating better descriptions",
            intended_task=task,
            executed="Created function to describe exported WP",
            executed_task=task,
            start= start, end=end)
        wp.save()

        exporter = agents.Exporter()
        exporter.export_logs([wp], ROOT_URL, 'adam', 'senha')
        
        content = self.get_list_of_submitted_logs()
        self.assertTrue(('Task id: 2376') in content)
        self.assertTrue('Log creator: 1' in content)
        self.assertTrue(('Date: %s' % start.strftime("%Y%m%d")) in content)
        self.assertTrue('Worked hours: %s' % wp.hours in content)
        self.assertTrue('Description: %s' % get_exported_description(wp) in content)

    def test_export_two_wps(self): 
        emp, task, start, end = self.get_depencencies()

        wp1 = WorkingPeriod(employee=emp,
            intended="Write a function for creating better descriptions",
            intended_task=task,
            executed="Created function to describe exported WP",
            executed_task=task,
            start= start, end=end)
        wp1.save()

        delta = timedelta(1)
        tomorrow_start=start+delta
        tomorrow_end=end+delta
        wp2 = WorkingPeriod(employee=emp,
            intended="Export stuff",
            intended_task=task,
            executed="Exporting WPs to old netuno",
            executed_task=task,
            start=tomorrow_start, end=tomorrow_end)
        wp2.save()



        exporter = agents.Exporter()
        exporter.export_logs([wp1, wp2], ROOT_URL, 'adam', 'senha')
        
        content = self.get_list_of_submitted_logs()
        self.assertTrue(('Task id: 2376') in content)
        self.assertTrue('Log creator: 1' in content)
        self.assertTrue(('Date: %s' % start.strftime("%Y%m%d")) in content)
        self.assertTrue('Worked hours: %s' % wp1.hours in content)
        self.assertTrue('Description: %s' % get_exported_description(wp1) in content)     
        self.assertTrue(('Task id: 2376') in content)
        self.assertTrue('Log creator: 1' in content)
        self.assertTrue(('Date: %s' % tomorrow_start.strftime("%Y%m%d")) in content)
        self.assertTrue('Worked hours: %s' % wp2.hours in content)
        self.assertTrue('Description: %s' % get_exported_description(wp2) in content)    

    def test_export_mark_as_exported(self): 
        emp, task, start, end = self.get_depencencies()

        wp = WorkingPeriod(employee=emp,
            intended="Write a function for creating better descriptions",
            intended_task=task,
            executed="Created function to describe exported WP",
            executed_task=task,
            start= start, end=end)
        wp.save()

        self.assertFalse(ExportedLog.is_exported(wp))

        exporter = agents.Exporter()
        exporter.export_logs([wp], ROOT_URL, 'adam', 'senha')
        
        content = self.get_list_of_submitted_logs()
        self.assertTrue(('Task id: 2376') in content)
        self.assertTrue('Log creator: 1' in content)
        self.assertTrue(('Date: %s' % start.strftime("%Y%m%d")) in content)
        self.assertTrue('Worked hours: %s' % wp.hours in content)
        self.assertTrue('Description: %s' % get_exported_description(wp) in content)

        self.assertTrue(ExportedLog.is_exported(wp))

    def test_marked_as_exported_not_exported_again(self): 
        emp, task, start, end = self.get_depencencies()

        wp1 = WorkingPeriod(employee=emp,
            intended="Write a function for creating better descriptions",
            intended_task=task,
            executed="Created function to describe exported WP",
            executed_task=task,
            start= start, end=end)
        wp1.save()

        tomorrow_start=start+timedelta(1)
        tomorrow_end=end+timedelta(1, 3600)
        wp2 = WorkingPeriod(employee=emp,
            intended="Export stuff",
            intended_task=task,
            executed="Exporting WPs to old netuno",
            executed_task=task,
            start=tomorrow_start, end=tomorrow_end)
        wp2.save()
        ExportedLog(working_period=wp2).save()

        self.assertFalse(ExportedLog.is_exported(wp1))
        self.assertTrue(ExportedLog.is_exported(wp2))

        exporter = agents.Exporter()
        exporter.export_logs([wp1, wp2], ROOT_URL, 'adam', 'senha')
        
        content = self.get_list_of_submitted_logs()
        self.assertTrue(('Task id: 2376') in content)
        self.assertTrue('Log creator: 1' in content)
        self.assertTrue(('Date: %s' % start.strftime("%Y%m%d")) in content)
        self.assertTrue('Worked hours: %s' % wp1.hours in content)
        self.assertTrue('Description: %s' % get_exported_description(wp1) in content)     
        self.assertFalse(('Date: %s' % tomorrow_start.strftime("%Y%m%d")) in content)
        self.assertFalse('Worked hours: %s' % wp2.hours in content)
        self.assertFalse('Description: %s' % get_exported_description(wp2) in content)  

    def test_does_not_export_incomplete(self): 
        emp, task, start, end = self.get_depencencies()

        wp1 = WorkingPeriod(employee=emp,
            intended="Write a function for creating better descriptions",
            intended_task=task,
            executed="Created function to describe exported WP",
            executed_task=task,
            start= start, end=end)
        wp1.save()

        wp2 = WorkingPeriod(employee=emp,
            intended="Export stuff",
            intended_task=task,
            executed="Exporting WPs to old netuno",
            executed_task=task,
            start=start) # No end
        wp2.save()

        wp3 = WorkingPeriod(employee=emp,
            intended="Thinking about future",
            intended_task=task,
            #executed="Exporting WPs to old netuno", # No final message
            executed_task=task,
            start=start, end=end)
        wp3.save()

        wp4 = WorkingPeriod(employee=emp,
            intended="PLanning how to spend money",
            intended_task=task,
            executed="Exporting WPs to old netuno",
            # executed_task=task, # No updated task
            start=start, end=end)
        wp4.save()

        wp5 = WorkingPeriod(employee=emp,
            intended="Write a function for creating better descriptions",
            intended_task=task,
            executed="Closing WP",
            executed_task=task,
            start= start, end=end)
        wp5.save()

        exporter = agents.Exporter()
        exporter.export_logs([wp1, wp2, wp3, wp4, wp5], ROOT_URL, 'adam', 'senha')
        
        content = self.get_list_of_submitted_logs()
        self.assertTrue(('Task id: 2376') in content)
        self.assertTrue('Log creator: 1' in content)
        self.assertTrue(('Date: %s' % start.strftime("%Y%m%d")) in content)
        self.assertTrue('Worked hours: %s' % wp1.hours in content)

        self.assertTrue('Description: %s' % get_exported_description(wp1) in content)     
        self.assertFalse('Description: %s' % get_exported_description(wp2) in content)     
        self.assertFalse('Description: %s' % get_exported_description(wp3) in content)     
        self.assertFalse('Description: %s' % get_exported_description(wp4) in content)     
        self.assertTrue('Description: %s' % get_exported_description(wp5) in content)     

        self.assertTrue(ExportedLog.is_exported(wp1))
        self.assertFalse(ExportedLog.is_exported(wp2))
        self.assertFalse(ExportedLog.is_exported(wp3))
        self.assertFalse(ExportedLog.is_exported(wp4))
        self.assertTrue(ExportedLog.is_exported(wp5))

    def setUp(self):
        NetunomockTestCase.setUp(self)
        ModelTestCase.setUp(self)
        
    def tearDown(self):
        NetunomockTestCase.tearDown(self)
        ModelTestCase.tearDown(self)

    def get_depencencies(self):
        emp = get_employee(get_organization())    
        agents.importer.import_all(ROOT_URL, 'adam', 'senha')

        e = ImportedEntity.objects.get(category='T', original_id=2376)
        task = Task.objects.get(id=e.new_id)
        start = datetime(2011, 12, 31, 8, 0)
        end = datetime(2011, 12, 31, 12, 0)
        return emp, task, start, end

    def get_list_of_submitted_logs(self):
        browser = mechanize.Browser()
        response = browser.open(ROOT_URL + SHOW_LOGS_PATH)
        return response.read().decode('utf-8')
