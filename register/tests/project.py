import unittest2 as unittest
from test_utilities import ModelTestCase, get_organization_project, get_employee

from register.models import Project

class ProjectTestCase(ModelTestCase):

    def setUp(self):
        (
            self.organization, 
            self.project
        ) = get_organization_project()
        self.employee = get_employee(self.organization)

    def is_archivable(self):
        self.assertFalse(self.project.archived)
        self.project.archive()
        self.assertTrue(self.project.archived)

    def save_archived_status(self):
        self.assertFalse(self.project.archived)
        self.project.archive()
        self.assertTrue(self.project.archived)

        project = Project.objects.get(id=self.project.id)
        self.assertFalse(project.archived)
        self.project.archive()
        self.project.save()

        project = Project.objects.get(id=self.project.id)
        self.assertTrue(project.archived)

projectTestSuite = unittest.TestSuite()
projectTestSuite.addTest(ProjectTestCase('is_archivable'))
projectTestSuite.addTest(ProjectTestCase('save_archived_status'))
