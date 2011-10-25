# -*- coding: utf-8 -*-
import os.path

import unittest2 as unittest

import importer.parser as parser
from importer.tests.util import ParserTestCase

class TaskParserTestCase(ParserTestCase):

    def get_leaf_task(self):
        task_page = self.get_sample_content('task.html');
        task = parser.get_task(task_page)

        self.assertEqual(task['type'], 'leaf')
        self.assertEqual(task['name'], u'OS02 - Arquitetura da Informação e Identidade Visual')
        self.assertEqual(task['original_id'], 2832)
        self.assertEqual(task['project_id'], 151)
        self.assertEqual(task['description'], '')        

    def get_parent_task(self):
        task_page = self.get_sample_content('supertask.html');
        task = parser.get_task(task_page)

        self.assertEqual(task['type'], 'parent')
        self.assertEqual(task['name'], u'1o Sprint')
        self.assertEqual(task['original_id'], 2207)
        self.assertEqual(task['project_id'], 108)
        self.assertEqual(task['description'], '')
        self.assertItemsEqual(task['subtasks_ids'], [2208, 2209, 2210])


    def get_subtask(self):
        task_page = self.get_sample_content('subtask.html');
        task = parser.get_task(task_page)

        self.assertEqual(task['type'], 'leaf')
        self.assertEqual(task['name'], u'Listagem das Missões')
        self.assertEqual(task['original_id'], 2208)
        self.assertEqual(task['project_id'], 108)
        self.assertEqual(task['description'], '') 

    def get_task_list(self):
        task_page = self.get_sample_content('tasks.html')
        tasks = parser.get_list_of_partial_tasks(task_page)

        self.assertEqual(len(tasks), 914)

        task = tasks[0]
        self.assertEqual(task['type'], 'partial')
        self.assertEqual(task['original_id'], 2376)

        task = tasks[44]
        self.assertEqual(task['type'], 'partial')
        self.assertEqual(task['original_id'], 2228)

        task = tasks[913]
        self.assertEqual(task['type'], 'partial')
        self.assertEqual(task['original_id'], 2114)

testSuite = unittest.TestSuite()
testSuite.addTest(TaskParserTestCase('get_leaf_task'))
testSuite.addTest(TaskParserTestCase('get_parent_task'))
testSuite.addTest(TaskParserTestCase('get_subtask'))
testSuite.addTest(TaskParserTestCase('get_task_list'))
