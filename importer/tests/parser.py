import os.path

import unittest2 as unittest

import importer.parser as parser
from importer.tests.util import ParserTestCase

class OrganizationParserTestCase(ParserTestCase):

    def get_something(self):
        companies_page = self.get_sample_content('companies.html');
        organizations = parser.get_organizations(companies_page)

        self.assertGreater(len(organizations), 0)

    def get_first_organizations(self):
        companies_page = self.get_sample_content('companies.html');
        organizations = parser.get_organizations(companies_page)

        self.assertEquals(len(organizations), 42)

        organization = organizations[0]
        self.assertEquals(organization['name'], "Ambar Tec")
        self.assertEquals(organization['original_id'], 4)
        self.assertEquals(organization['description'], "")

        organization = organizations[1]
        self.assertEquals(organization['name'], "Anprotec")
        self.assertEquals(organization['original_id'], 16)
        self.assertEquals(organization['description'], """Katia Sitta Fortini
Coordenadora de Atendimento e Relacionamento ANPROTEC
telefone 8427.1420""")

    def get_last_organization(self):
        companies_page = self.get_sample_content('companies.html');
        organizations = parser.get_organizations(companies_page)

        self.assertEquals(len(organizations), 42)

        organization = organizations[-1]
        self.assertEquals(organization['name'], "Zilics")
        self.assertEquals(organization['original_id'], 26)
        self.assertEquals(organization['description'], "")


testSuite = unittest.TestSuite()
testSuite.addTest(OrganizationParserTestCase('get_something'))
testSuite.addTest(OrganizationParserTestCase('get_first_organizations'))
testSuite.addTest(OrganizationParserTestCase('get_last_organization'))
