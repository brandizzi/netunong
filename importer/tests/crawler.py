import os.path
from multiprocessing import Process
import time
import unittest2 as unittest

from importer.crawler import NetunoCrawler
from importer.parser import get_companies, get_users

from netunomock.server import run_server, ROOT_URL

class CrawlerTestCase(unittest.TestCase):

    def setUp(self):
        self.server = Process(target=run_server)
        self.server.start()

    def tearDown(self):
        self.server.terminate()

    def login(self):
        crawler = NetunoCrawler(ROOT_URL)
        self.assertFalse(crawler.logged_in)

        crawler.login(username='adam', password='senha')
        self.assertTrue(crawler.logged_in)

        crawler.logout()
        self.assertFalse(crawler.logged_in)
        crawler.login(username='nobody', password='false password')
        self.assertFalse(crawler.logged_in)

        crawler.login(username='adam', password='senha')
        self.assertTrue(crawler.logged_in)        

    def select_companies(self):
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

    def select_user_from_companies(self):
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

testSuite = unittest.TestSuite()
testSuite.addTest(CrawlerTestCase('login'))
testSuite.addTest(CrawlerTestCase('select_companies'))
testSuite.addTest(CrawlerTestCase('select_user_from_companies'))
