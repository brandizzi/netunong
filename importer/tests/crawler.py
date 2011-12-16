import os.path
from multiprocessing import Process
import time
import unittest2 as unittest

from importer.crawler import NetunoCrawler
from importer.parser import get_companies

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

testSuite = unittest.TestSuite()
testSuite.addTest(CrawlerTestCase('login'))
testSuite.addTest(CrawlerTestCase('select_companies'))
