# -*- coding: utf-8 -*-
import os.path

import unittest2 as unittest

import importer.parser as parser
from importer.tests.util import ParserTestCase

import settings

class UserParserTestCase(ParserTestCase):

    def get_something(self):
        users_page = self.get_sample_content('company_users.html');
        users = parser.get_users(users_page)

        self.assertGreater(len(users), 0)

    def get_first_users(self):
        users_page = self.get_sample_content('company_users.html');
        users = parser.get_users(users_page)

        self.assertEquals(len(users), 60)

        user = users[0]
        self.assertEquals(user['username'], "mabreu")
        self.assertEquals(user['original_id'], 13)
        self.assertEquals(user['first_name'], 'Marianne')
        self.assertEquals(user['middle_name'], "")
        self.assertEquals(user['last_name'], 'Abreu')
        self.assertEquals(user['email'], 'mabreu@'+settings.NETUNONG_EMAIL_DOMAIN)
        self.assertEquals(user['password'], 'mabreu')
        self.assertEquals(user['company_id'], 1)

        user = users[5]
        self.assertEquals(user['username'], "danilo.avila")
        self.assertEquals(user['original_id'], 157)
        self.assertEquals(user['first_name'], 'Danilo')
        self.assertEquals(user['middle_name'], u"Ávila Monte Cristo")
        self.assertEquals(user['last_name'], u'Ferreira')
        self.assertEquals(user['email'], 'danilo.avila@'+settings.NETUNONG_EMAIL_DOMAIN)
        self.assertEquals(user['password'], 'danilo.avila')
        self.assertEquals(user['company_id'], 1)

    def get_last_user(self):
        users_page = self.get_sample_content('company_users.html');
        users = parser.get_users(users_page)

        self.assertEquals(len(users), 60)

        user = users[-1]
        self.assertEquals(user['username'], "msousa")
        self.assertEquals(user['original_id'], 6)
        self.assertEquals(user['first_name'], 'Marcelo')
        self.assertEquals(user['middle_name'], "")
        self.assertEquals(user['last_name'], 'Zouza')
        self.assertEquals(user['email'], 'msousa@'+settings.NETUNONG_EMAIL_DOMAIN)
        self.assertEquals(user['password'], 'msousa')
        self.assertEquals(user['company_id'], 1)

testSuite = unittest.TestSuite()
testSuite.addTest(UserParserTestCase('get_something'))
testSuite.addTest(UserParserTestCase('get_first_users'))
testSuite.addTest(UserParserTestCase('get_last_user'))
