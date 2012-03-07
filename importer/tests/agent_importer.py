import threading
import time

from importer.models import ImportedEntity
from register.models import Organization, Project, Task, Employee
from importer.agent import Importer, ORGANIZATIONS, EMPLOYEES, PROJECTS, TASKS
import importer.agent as agent

from importer.tests.util import NetunomockTestCase, ModelTestCase

from netunomock.server import ROOT_URL

class ImporterTestCase(NetunomockTestCase, ModelTestCase):

    def test_import_companies(self):
        self.assertEqual(0, len(ImportedEntity.objects.all()))
        self.assertEqual(0, len(Organization.objects.all()))
        
        importer = Importer(ROOT_URL, 'adam', 'senha')
        importer.import_organizations()
        
        self.assertEqual(43, len(ImportedEntity.objects.all()))
        self.assertEqual(43, len(Organization.objects.all()))

    def test_import_companies_users(self):
        self.assertEqual(0, len(ImportedEntity.objects.all()))
        self.assertEqual(0, len(Organization.objects.all()))
        
        importer = Importer(ROOT_URL, 'adam', 'senha')
        importer.import_organizations()
        importer.import_employees()
        
        self.assertEqual(43+80, len(ImportedEntity.objects.all()))
        self.assertEquals(80, len(ImportedEntity.objects.filter(category='U')))
        self.assertEqual(80, len(Employee.objects.all()))


    def test_import_companies_projects(self):
        self.assertEqual(0, len(ImportedEntity.objects.all()))
        self.assertEqual(0, len(Project.objects.all()))
        
        importer = Importer(ROOT_URL, 'adam', 'senha')
        importer.import_organizations()
        importer.import_projects()
        
        self.assertEqual(43+104, len(ImportedEntity.objects.all()))
        self.assertEquals(104, len(ImportedEntity.objects.filter(category='P')))
        self.assertEqual(104, len(Project.objects.all()))

    def test_import_companies_users_projects_tasks(self):
        self.assertEqual(0, len(ImportedEntity.objects.all()))
        self.assertEqual(0, len(Organization.objects.all()))
        self.assertEqual(0, len(Employee.objects.all()))
        self.assertEqual(0, len(Project.objects.all()))
        
        importer = Importer(ROOT_URL, 'adam', 'senha')
        importer.import_organizations()
        importer.import_employees()
        importer.import_projects()
        importer.import_tasks()

        self.assertEquals(8, len(ImportedEntity.objects.filter(category='T')))
        self.assertEqual(8, len(Task.objects.all()))

    def test_give_feedback(self):
        self.assertEqual(0, len(ImportedEntity.objects.all()))
        self.assertEqual(0, len(Organization.objects.all()))
        self.assertEqual(0, len(Employee.objects.all()))
        self.assertEqual(0, len(Project.objects.all()))
        self.assertEqual(0, len(Task.objects.all()))
        
        importer = Importer(ROOT_URL, 'adam', 'senha')
        self.assertEqual([], importer.already_done)

        importer.import_organizations()
        self.assertEqual([ORGANIZATIONS], importer.already_done)
        importer.import_employees()
        self.assertItemsEqual([ORGANIZATIONS, EMPLOYEES], importer.already_done)
        importer.import_projects()
        self.assertItemsEqual([ORGANIZATIONS, EMPLOYEES, PROJECTS],
                importer.already_done)
        importer.import_tasks()
        self.assertItemsEqual([ORGANIZATIONS, EMPLOYEES, PROJECTS, TASKS],
                importer.already_done)

    def test_import_all(self):
        self.assertEqual(0, len(ImportedEntity.objects.all()))
        self.assertEqual(0, len(Organization.objects.all()))
        self.assertEqual(0, len(Employee.objects.all()))
        self.assertEqual(0, len(Project.objects.all()))
        self.assertEqual(0, len(Task.objects.all()))
        
        importer = Importer(ROOT_URL, 'adam', 'senha')
        importer.import_all()

        self.assertEqual(43, len(ImportedEntity.objects.filter(category='C')))
        self.assertEqual(43, len(Organization.objects.all()))
        self.assertEquals(80, len(ImportedEntity.objects.filter(category='U')))
        self.assertEqual(80, len(Employee.objects.all()))
        self.assertEquals(104, len(ImportedEntity.objects.filter(category='P')))
        self.assertEqual(104, len(Project.objects.all()))
        self.assertEquals(8, len(ImportedEntity.objects.filter(category='T')))
        self.assertEqual(8, len(Task.objects.all()))

    def test_import_all_accepts_url_username_password(self):
        self.assertEqual(0, len(ImportedEntity.objects.all()))
        self.assertEqual(0, len(Organization.objects.all()))
        self.assertEqual(0, len(Employee.objects.all()))
        self.assertEqual(0, len(Project.objects.all()))
        self.assertEqual(0, len(Task.objects.all()))
        
        importer = Importer('', 'foo', 'bar')
        with self.assertRaises(Exception):
            importer.import_all()

        importer.import_all(ROOT_URL, 'adam', 'senha')

        self.assertEqual(43, len(ImportedEntity.objects.filter(category='C')))
        self.assertEqual(43, len(Organization.objects.all()))
        self.assertEquals(80, len(ImportedEntity.objects.filter(category='U')))
        self.assertEqual(80, len(Employee.objects.all()))
        self.assertEquals(104, len(ImportedEntity.objects.filter(category='P')))
        self.assertEqual(104, len(Project.objects.all()))
        self.assertEquals(8, len(ImportedEntity.objects.filter(category='T')))
        self.assertEqual(8, len(Task.objects.all()))

    def test_import_all_reports_importer_is_running(self):
        time.sleep(1)
        self.assertEqual(0, len(ImportedEntity.objects.all()))
        self.assertEqual(0, len(Organization.objects.all()))
        self.assertEqual(0, len(Employee.objects.all()))
        self.assertEqual(0, len(Project.objects.all()))
        self.assertEqual(0, len(Task.objects.all()))
        
        importer = Importer(ROOT_URL, 'adam', 'senha')
        self.assertFalse(importer.is_running)

        thread = threading.Thread(target=importer.import_all)
        thread.start()
        time.sleep(0.1)
        self.assertTrue(importer.is_running)
        time.sleep(2)
        self.assertTrue(importer.is_running)

        thread.join()
        
        self.assertFalse(importer.is_running)
        
        self.assertEqual(43, len(ImportedEntity.objects.filter(category='C')))
        self.assertEqual(43, len(Organization.objects.all()))
        self.assertEquals(80, len(ImportedEntity.objects.filter(category='U')))
        self.assertEqual(80, len(Employee.objects.all()))
        self.assertEquals(104, len(ImportedEntity.objects.filter(category='P')))
        self.assertEqual(104, len(Project.objects.all()))
        self.assertEquals(8, len(ImportedEntity.objects.filter(category='T')))
        self.assertEqual(8, len(Task.objects.all()))

    def test_import_all_reports_importer_is_running_and_block_others(self):
        self.assertEqual(0, len(ImportedEntity.objects.all()))
        self.assertEqual(0, len(Organization.objects.all()))
        self.assertEqual(0, len(Employee.objects.all()))
        self.assertEqual(0, len(Project.objects.all()))
        self.assertEqual(0, len(Task.objects.all()))
        
        importer = Importer(ROOT_URL, 'adam', 'senha')
        self.assertFalse(importer.is_running)

        thread1 = threading.Thread(target=importer.import_all)
        thread1.start()
        time.sleep(0.1)
        self.assertTrue(importer.is_running)
        time.sleep(2)
        self.assertTrue(importer.is_running)

        # Tries to run again
        thread2 = threading.Thread(target=importer.import_all)
        thread2.start()
        time.sleep(0.1)
        self.assertTrue(importer.is_running)
        time.sleep(0)
        self.assertFalse(thread2.is_alive())

        thread1.join()
        
        self.assertFalse(importer.is_running)
        
        self.assertEqual(43, len(ImportedEntity.objects.filter(category='C')))
        self.assertEqual(43, len(Organization.objects.all()))
        self.assertEquals(80, len(ImportedEntity.objects.filter(category='U')))
        self.assertEqual(80, len(Employee.objects.all()))
        self.assertEquals(104, len(ImportedEntity.objects.filter(category='P')))
        self.assertEqual(104, len(Project.objects.all()))
        self.assertEquals(8, len(ImportedEntity.objects.filter(category='T')))
        self.assertEqual(8, len(Task.objects.all()))


    def test_has_a_singleton_importer(self):
        self.assertEqual(0, len(ImportedEntity.objects.all()))
        self.assertEqual(0, len(Organization.objects.all()))
        self.assertEqual(0, len(Employee.objects.all()))
        self.assertEqual(0, len(Project.objects.all()))
        self.assertEqual(0, len(Task.objects.all()))
        
        self.assertIsNotNone(agent.importer)
        agent.importer.import_all(ROOT_URL, 'adam', 'senha')

        self.assertEqual(43, len(ImportedEntity.objects.filter(category='C')))
        self.assertEqual(43, len(Organization.objects.all()))
        self.assertEquals(80, len(ImportedEntity.objects.filter(category='U')))
        self.assertEqual(80, len(Employee.objects.all()))
        self.assertEquals(104, len(ImportedEntity.objects.filter(category='P')))
        self.assertEqual(104, len(Project.objects.all()))
        self.assertEquals(8, len(ImportedEntity.objects.filter(category='T')))
        self.assertEqual(8, len(Task.objects.all()))

    def setUp(self):
        NetunomockTestCase.setUp(self)
        ModelTestCase.setUp(self)
        
    def tearDown(self):
        NetunomockTestCase.tearDown(self)
        ModelTestCase.tearDown(self)

