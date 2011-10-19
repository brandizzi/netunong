# -*- coding: utf-8 -*-
import os.path

import unittest2 as unittest

import importer.parser as parser
from importer.tests.util import ParserTestCase

class TaskParserTestCase(ParserTestCase):

    def get_task(self):
        task_page = self.get_sample_content('task.html');
        task = parser.get_task(task_page)

        self.assertEqual(task['type'], 'leaf')
        self.assertEqual(task['name'], u'OS02 - Arquitetura da Informação e Identidade Visual')
        self.assertEqual(task['project_id'], 151)
        self.assertEqual(task['description'], '')        

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
testSuite.addTest(TaskParserTestCase('get_task'))
#testSuite.addTest(TaskParserTestCase('get_first_projects'))
#testSuite.addTest(TaskParserTestCase('get_last_project'))
