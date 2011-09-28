import os.path

import unittest2 as unittest

import importer.parser as parser
from importer.tests.util import ParserTestCase

class ProjectParserTestCase(ParserTestCase):

    def get_something(self):
        projects_page = self.get_sample_content('projects.html');
        projects = parser.get_projects(projects_page)

        self.assertGreater(len(projects), 0)

    def get_first_projects(self):
        projects_page = self.get_sample_content('projects.html');
        projects = parser.get_projects(projects_page)

        self.assertEquals(len(projects), 101)


        project = projects[0]
        self.assertEquals(project['name'], "Feedbackme")
        self.assertEquals(project['original_id'], 116)
        self.assertEquals(project['company_id'], 1)
        self.assertEquals(project['description'], "")

        project = projects[1]
        self.assertEquals(project['name'], "SixPro")
        self.assertEquals(project['original_id'], 122)
        self.assertEquals(project['company_id'], 38)
        self.assertEquals(project['description'], "")

    def get_last_project(self):
        projects_page = self.get_sample_content('projects.html');
        projects = parser.get_projects(projects_page)

        self.assertEquals(len(projects), 101)

        project = projects[-1]
        self.assertEquals(project['name'], "TRT-14 Liferay")
        self.assertEquals(project['original_id'], 150)
        self.assertEquals(project['company_id'], 43)
        self.assertEquals(project['description'], "")


testSuite = unittest.TestSuite()
testSuite.addTest(ProjectParserTestCase('get_something'))
testSuite.addTest(ProjectParserTestCase('get_first_projects'))
testSuite.addTest(ProjectParserTestCase('get_last_project'))
