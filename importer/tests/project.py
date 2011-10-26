import os.path

import unittest2 as unittest

from register.models import Project, Organization
from importer.models import ImportedEntity

from importer.tests.util import ImportedEntityTestCase

class ProjectSavingTestCase(ImportedEntityTestCase):

    def save_projects(self):
        # needed
        companies = [
            {'name': 'org1', 'original_id': 4, 'description': 'Organization 1'},
            {'name': 'org2', 'original_id': 8, 'description': 'Organization 2'},
        ]
        ImportedEntity.import_companies_as_organizations(companies)

        projects = [
            {'name': 'proj1', 'original_id': 1, 'company_id': 4, 'description': ''},
            {'name': 'proj2', 'original_id': 2, 'company_id': 4, 'description': ''},
            {'name': 'proj3', 'original_id': 3, 'company_id': 8, 'description': ''},
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
            company_entity = ImportedEntity.objects.get(
                    category='C', original_id=project_dict['company_id'])
            organization = Organization.objects.get(id=company_entity.new_id)
            self.assertEquals(organization, project.organization)

    def save_only_new_projects(self):
        # needed
        companies = [
            {'name': 'org1', 'original_id': 4, 'description': 'Organization 1'},
            {'name': 'org2', 'original_id': 8, 'description': 'Organization 2'},
        ]
        ImportedEntity.import_companies_as_organizations(companies)

        projects = [
            {'name': 'proj1', 'original_id': 1, 'company_id': 4, 'description': ''},
        ]
        ImportedEntity.import_projects(projects)
        
        entities = ImportedEntity.objects.filter(category='P')
        # Not new under the sun
        self.assertEquals(1, len(entities))
        entity, project_dict = entities[0], projects[0]
        self.assertEquals('P', entity.category)
        self.assertEquals('project', entity.get_category_display())
        self.assertEquals(project_dict['original_id'], entity.original_id)

        project = Project.objects.get(id=entity.new_id)
        self.assertEquals(project_dict['name'], project.name)
        self.assertEquals(project_dict['description'], project.description)
        company_entity = ImportedEntity.objects.get(
                category='C', original_id=project_dict['company_id'])
        organization = Organization.objects.get(id=company_entity.new_id)
        self.assertEquals(organization, project.organization)

        # Now... THE PARTY BEGINS!
        projects += [
            {'name': 'proj2', 'original_id': 2, 'company_id': 4, 'description': ''},
            {'name': 'proj3', 'original_id': 3, 'company_id': 8, 'description': ''},
        ]

        ImportedEntity.import_projects(projects)
        entities = ImportedEntity.objects.filter(category='P')
        # Should be 3, not 4
        self.assertEquals(3, len(entities))
        for entity, project_dict in zip(entities, projects):
            self.assertEquals('P', entity.category)
            self.assertEquals('project', entity.get_category_display())
            self.assertEquals(project_dict['original_id'], entity.original_id)

            project = Project.objects.get(id=entity.new_id)
            self.assertEquals(project_dict['name'], project.name)
            self.assertEquals(project_dict['description'], project.description)
            company_entity = ImportedEntity.objects.get(
                    category='C', original_id=project_dict['company_id'])
            organization = Organization.objects.get(id=company_entity.new_id)
            self.assertEquals(organization, project.organization)



testSuite = unittest.TestSuite()
testSuite.addTest(ProjectSavingTestCase('save_projects'))
testSuite.addTest(ProjectSavingTestCase('save_only_new_projects'))
