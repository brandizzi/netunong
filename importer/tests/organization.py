import os.path

import unittest2 as unittest

from register.models import Organization
from importer.models import ImportedEntity

class OrganizationSavingTestCase(unittest.TestCase):

    def save_companies_as_organizations(self):
        companies = [
            {'name': 'org1', 'original_id': 1, 'description': 'Organization 1'},
            {'name': 'org2', 'original_id': 2, 'description': 'Organization 2'},
            {'name': 'org3', 'original_id': 3, 'description': 'Organization 3'}
        ]
        ImportedEntity.import_companies_as_organizations(companies)

        entities = ImportedEntity.objects.all()
        self.assertEquals(3, len(entities))
        for entity, company in zip(entities, companies):
            self.assertEquals('C', entity.category)
            self.assertEquals('company', entity.get_category_display())
            self.assertEquals(company['original_id'], entity.original_id)

    def f():
            organization = Organization.objects.get(id=entity.new_id)
            self.assertEquals(company['name'], organization.name)
            self.assertEquals(company['description'], organization.description)
        


testSuite = unittest.TestSuite()
testSuite.addTest(OrganizationSavingTestCase('save_companies_as_organizations'))
#testSuite.addTest(OrganizationSavingTestCase('get_first_organizations'))
#testSuite.addTest(OrganizationSavingTestCase('get_last_organization'))
