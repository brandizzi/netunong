import os.path
from multiprocessing import Process
import time
import unittest2 as unittest

from importer.crawler import NetunoCrawler

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


testSuite = unittest.TestSuite()
testSuite.addTest(CrawlerTestCase('login'))
