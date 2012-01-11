import os.path

import importer.parser as parser
from importer.tests.util import ParserTestCase

class CompanyParserTestCase(ParserTestCase):

    def test_get_something(self):
        companies_page = self.get_sample_content('companies.html');
        companies = parser.get_companies(companies_page)

        self.assertGreater(len(companies), 0)

    def test_get_first_companies(self):
        companies_page = self.get_sample_content('companies.html');
        companies = parser.get_companies(companies_page)

        self.assertEquals(len(companies), 42)

        company = companies[0]
        self.assertEquals(company['name'], "Ambar Tec")
        self.assertEquals(company['original_id'], 4)
        self.assertEquals(company['description'], "")

        company = companies[1]
        self.assertEquals(company['name'], "Anprotec")
        self.assertEquals(company['original_id'], 16)
        self.assertEquals(company['description'], """Katia Sitta Fortini
Coordenadora de Atendimento e Relacionamento ANPROTEC
telefone 8427.1420""")

    def test_get_last_company(self):
        companies_page = self.get_sample_content('companies.html');
        companies = parser.get_companies(companies_page)

        self.assertEquals(len(companies), 42)

        company = companies[-1]
        self.assertEquals(company['name'], "Zilics")
        self.assertEquals(company['original_id'], 26)
        self.assertEquals(company['description'], "")

