from test_utilities import ModelTestCase, get_organization_project, get_employee

from register.models import Project

class ProjectTestCase(ModelTestCase):

    def setUp(self):
        (
            self.organization, 
            self.project
        ) = get_organization_project()
        self.employee = get_employee(self.organization)

    def test_is_completable(self):
        self.assertFalse(self.project.completed)
        self.project.complete()
        self.assertTrue(self.project.completed)

    def test_save_completed_status(self):
        self.assertFalse(self.project.completed)
        self.project.complete()
        self.assertTrue(self.project.completed)

        project = Project.objects.get(id=self.project.id)
        self.assertFalse(project.completed)
        self.project.complete()
        self.project.save()

        project = Project.objects.get(id=self.project.id)
        self.assertTrue(project.completed)

