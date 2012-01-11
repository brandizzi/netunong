import os.path

from register.models import Task
from importer.models import ImportedEntity, SavingParentTask

from importer.tests.util import ImportedEntityTestCase

class TaskSavingTestCase(ImportedEntityTestCase):

    def test_save_leaf_task(self):
        # Setting up
        companies = [
            {'name': 'org1', 'original_id': 1, 'description': 'Organization 1'},
            {'name': 'org2', 'original_id': 2, 'description': 'Organization 2'},
        ]
        ImportedEntity.import_companies_as_organizations(companies)
        projects = [
            {'name': 'proj1', 'original_id': 1, 'company_id': 1, 'description': ''},
            {'name': 'proj2', 'original_id': 2, 'company_id': 1, 'description': ''},
            {'name': 'proj3', 'original_id': 3, 'company_id': 2, 'description': ''},
        ]
        ImportedEntity.import_projects(projects)

        # Not let us go!
        task_dict = {
                'type' : 'leaf', 'name' : 'Leaf Task', 'original_id' : 33,
                'project_id' : projects[0]['original_id'],
                'description' : '', 'subtasks_ids' : []
        }
        ImportedEntity.import_task(task_dict)

        entities = ImportedEntity.objects.filter(category='T')
        self.assertEquals(1, len(entities))
        entity = entities[0]
        self.assertEquals('T', entity.category)
        self.assertEquals('task', entity.get_category_display())
        self.assertEquals(task_dict['original_id'], entity.original_id)

        task = Task.objects.get(id=entity.new_id)
        self.assertEquals(task_dict['name'], task.name)
        self.assertEquals(task_dict['description'], task.description)
        self.assertEquals(task_dict['project_id'], task.project.id)

    def test_test_save_parent_task(self):
        # Setting up
        companies = [
            {'name': 'org1', 'original_id': 1, 'description': 'Organization 1'},
            {'name': 'org2', 'original_id': 2, 'description': 'Organization 2'},
        ]
        ImportedEntity.import_companies_as_organizations(companies)
        projects = [
            {'name': 'proj1', 'original_id': 1, 'company_id': 1, 'description': ''},
            {'name': 'proj2', 'original_id': 2, 'company_id': 1, 'description': ''},
            {'name': 'proj3', 'original_id': 3, 'company_id': 2, 'description': ''},
        ]
        ImportedEntity.import_projects(projects)

        # Not let us go!
        task_dict = {
                'type' : 'parent', 'name' : 'Parent Task', 'original_id' : 34,
                'project_id' : projects[1]['original_id'],
                'description' : '', 'subtasks_ids' : [35, 36]
        }
        ImportedEntity.import_task(task_dict)

        entities = ImportedEntity.objects.filter(category='T')
        self.assertEquals(1, len(entities))

    def test_save_only_once(self):
        # Setting up
        companies = [
            {'name': 'org1', 'original_id': 1, 'description': 'Organization 1'},
        ]
        ImportedEntity.import_companies_as_organizations(companies)
        projects = [
            {'name': 'proj1', 'original_id': 1, 'company_id': 1, 'description': ''},
        ]
        ImportedEntity.import_projects(projects)

        # Not let us go!
        task_dict = {
                'type' : 'leaf', 'name' : 'Leaf Task', 'original_id' : 33,
                'project_id' : projects[0]['original_id'],
                'description' : '', 'subtasks_ids' : []
        }
        ImportedEntity.import_task(task_dict)
        # As usual
        entities = ImportedEntity.objects.filter(category='T')
        self.assertEquals(1, len(entities))
        entity = entities[0]
        self.assertEquals('T', entity.category)
        self.assertEquals('task', entity.get_category_display())
        self.assertEquals(task_dict['original_id'], entity.original_id)

        task = Task.objects.get(id=entity.new_id)
        self.assertEquals(task_dict['name'], task.name)
        self.assertEquals(task_dict['description'], task.description)
        self.assertEquals(task_dict['project_id'], task.project.id)
        # import again
        ImportedEntity.import_task(task_dict)
        # Should be still only 1
        entities = ImportedEntity.objects.filter(category='T')
        self.assertEquals(1, len(entities))
        # Should be equal to previous
        self.assertEquals(entity, entities[0])


