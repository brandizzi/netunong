import os.path

import unittest2 as unittest

from register.models import Project
from importer.models import ImportedEntity

from importer.tests.util import ImportedEntityTestCase

class ProjectSavingTestCase(ImportedEntityTestCase):

    def save_projects(self):
        # needed
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
        
        entities = ImportedEntity.objects.filter(category='P')
        self.assertEquals(3, len(entities))
        for entity, project_dict in zip(entities, projects):
            self.assertEquals('P', entity.category)
            self.assertEquals('project', entity.get_category_display())
            self.assertEquals(project_dict['original_id'], entity.original_id)

            project = Project.objects.get(id=entity.new_id)
            self.assertEquals(project_dict['name'], project.name)
            self.assertEquals(project_dict['description'], project.description)
            self.assertEquals(project_dict['company_id'], project.organization.id)

testSuite = unittest.TestSuite()
testSuite.addTest(ProjectSavingTestCase('save_projects'))
