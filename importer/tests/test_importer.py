import unittest2 as unittest

from importer.models import ImportedEntity
from register.models import Organization, Project, Task, Employee
from importer.agent import Importer

from importer.tests.util import NetunomockTestCase, ImportedEntityTestCase
from netunomock.server import ROOT_URL

class ImporterTestCase(NetunomockTestCase, ImportedEntityTestCase):

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

    def test_import_companies_users(self):
        self.assertEqual(0, len(ImportedEntity.objects.all()))
        self.assertEqual(0, len(Employee.objects.all()))
        
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

        self.assertEquals(162, len(ImportedEntity.objects.filter(category='T')))
        self.assertEqual(162, len(Task.objects.all()))

    def setUp(self):
        NetunomockTestCase.setUp(self)
        ImportedEntityTestCase.setUp(self)
        
    def tearDown(self):
        NetunomockTestCase.tearDown(self)
        ImportedEntityTestCase.tearDown(self)

testSuite = unittest.TestSuite()
testSuite.addTest(ImporterTestCase('test_import_companies'))
testSuite.addTest(ImporterTestCase('test_import_companies_users'))
testSuite.addTest(ImporterTestCase('test_import_companies_projects'))
testSuite.addTest(ImporterTestCase('test_import_companies_users_projects_tasks'))
