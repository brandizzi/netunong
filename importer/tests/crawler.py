# -*- coding: utf-8 -*-
from importer.crawler import NetunoCrawler, AuthenticationException
from importer.parser import get_companies, get_users, get_projects, \
        get_list_of_partial_tasks, get_task, is_parent_task
from importer.tests.util import NetunomockTestCase

from netunomock.server import ROOT_URL

class CrawlerTestCase(NetunomockTestCase):

    def test_login(self):
        crawler = NetunoCrawler(ROOT_URL)
        self.assertFalse(crawler.logged_in)

        crawler.login(username='adam', password='senha')
        self.assertTrue(crawler.logged_in)

        crawler.logout()
        self.assertFalse(crawler.logged_in)
        with self.assertRaises(AuthenticationException):
            crawler.login(username='nobody', password='false password')
        self.assertFalse(crawler.logged_in)

        crawler.login(username='adam', password='senha')
        self.assertTrue(crawler.logged_in)        

    def test_select_companies(self):
        crawler = NetunoCrawler(ROOT_URL)
        crawler.login(username='adam', password='senha')
        self.assertTrue(crawler.logged_in)

        crawler.go_to_all_companies()
        companies = get_companies(crawler.content)
        self.assertEquals(len(companies), 43)

        company = companies[0]
        self.assertEquals(company['name'], "Ambar Tec")
        self.assertEquals(company['original_id'], 4)
        self.assertEquals(company['description'], "")

        company = companies[1]
        self.assertEquals(company['name'], "Anprotec")
        self.assertEquals(company['original_id'], 16)

        company = companies[-1]
        self.assertEquals(company['name'], "Zilics")
        self.assertEquals(company['original_id'], 26)

    def test_select_user_from_companies(self):
        crawler = NetunoCrawler(ROOT_URL)
        crawler.login(username='adam', password='senha')
        self.assertTrue(crawler.logged_in)

        crawler.go_to_all_companies()
        companies = get_companies(crawler.content)
        self.assertEquals(len(companies), 43)

        company = companies[0]
        crawler.go_to_users_from_company(company['original_id'])
        users = get_users(crawler.content)
        self.assertEquals(len(users), 1)

        user = users[0]
        self.assertEquals(user['original_id'], 20)
        self.assertEquals(user['username'], 'lamatuzzi')
        self.assertEquals(user['first_name'], 'Luciano')
        self.assertEquals(user['last_name'], 'Teixeira')
        self.assertEquals(user['middle_name'], 'Amatuzzi')

        # SEA
        company = companies[26]
        crawler.go_to_users_from_company(company['original_id'])
        users = get_users(crawler.content)
        self.assertEquals(len(users), 60)

        user = users[0]
        self.assertEquals(user['original_id'], 13)
        self.assertEquals(user['username'], 'mabreu')
        self.assertEquals(user['first_name'], 'Marianne')
        self.assertEquals(user['last_name'], 'Abreu')
        self.assertEquals(user['middle_name'], '')

        user = users[59]
        self.assertEquals(user['original_id'], 6)
        self.assertEquals(user['username'], 'msousa')
        self.assertEquals(user['first_name'], 'Marcelo')
        self.assertEquals(user['last_name'], 'Zouza')
        self.assertEquals(user['middle_name'], '')

    def test_select_projects(self):
        crawler = NetunoCrawler(ROOT_URL)
        crawler.login(username='adam', password='senha')
        self.assertTrue(crawler.logged_in)

        crawler.go_to_all_projects()
        projects = get_projects(crawler.content)
        self.assertEquals(104, len(projects))

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

        project = projects[-1]
        self.assertEquals(project['name'], "Liferay")
        self.assertEquals(project['original_id'], 158)
        self.assertEquals(project['company_id'], 48)
        self.assertEquals(project['description'], "")

    def test_select_tasks(self):
        crawler = NetunoCrawler(ROOT_URL)
        crawler.login(username='adam', password='senha')
        self.assertTrue(crawler.logged_in)

        crawler.go_to_all_tasks()
        tasks = get_list_of_partial_tasks(crawler.content)
        self.assertEquals(58, len(tasks))

        task = tasks[0]
        self.assertEqual(task['type'], 'partial')
        self.assertEqual(task['original_id'], 2376)

        task = tasks[-1]
        self.assertEqual(task['type'], 'partial')
        self.assertEqual(task['original_id'], 2114)

    def test_select_specific_task(self):
        crawler = NetunoCrawler(ROOT_URL)
        crawler.login(username='adam', password='senha')
        self.assertTrue(crawler.logged_in)

        crawler.go_to_all_tasks()
        tasks = get_list_of_partial_tasks(crawler.content)
        self.assertEquals(58, len(tasks))

        partial_task = tasks[0]
        crawler.go_to_task(partial_task['original_id'])
        task = get_task(crawler.content)
        self.assertEqual(task['type'], u'leaf')
        self.assertEqual(task['original_id'], 2376)
        self.assertEqual(task['project_id'], 118)
        self.assertEqual(task['name'], u'Reuniões')

        partial_task = tasks[7]
        crawler.go_to_task(partial_task['original_id'])
        task = get_task(crawler.content)
        self.assertEqual(task['type'], u'parent')
        self.assertEqual(task['original_id'], 2207)
        self.assertEqual(task['project_id'], 108)
        self.assertEqual(task['name'], u'1o Sprint')


        partial_task = tasks[-1]
        crawler.go_to_task(partial_task['original_id'])
        task = get_task(crawler.content)
        self.assertEqual(task['type'], u'leaf')
        self.assertEqual(task['original_id'], 2114)
        self.assertEqual(task['project_id'], 55)
        self.assertEqual(task['name'], u'Release 0.9')

