# -*- coding: utf-8 -*-
import os
from cStringIO import StringIO
from importer.parser import is_parent_task, PARENT_TAG
import mechanize

def greeting():
    return u'Bem-vind'
    
class NetunoCrawler(object):

    def __init__(self, url):
        #set_output(file(os.devnull, 'w'))
        self.logged_in = False
        self.url = url
        self.browser = mechanize.Browser()
        self.content = ''

    def login(self, username, password):
        self.browser.open(self.url)
        self.browser.select_form(name="loginform")
        self.browser['username'] = username
        self.browser['password'] = password
        response = self.browser.submit()
        self.content = response.read().decode('utf-8')
        if greeting() in self.content:
            self.logged_in = True
        else:
            raise AuthenticationException("Authentication failed")

    def logout(self):
        response = self.browser.open(self.url+'/index.php?logout=-1')
        self.content = response.read().decode('utf-8')
        if 'loginform' in self.content:
            self.logged_in = False

    def go_to_all_companies(self):
        self.browser.open(self.url+'?m=companies')
        self.browser.select_form('searchform')
        self.browser['owner_filter_id'] = ['0']
        response = self.browser.submit()
        self.content = response.read().decode('utf-8')

    def go_to_users_from_company(self, company_id):
        url = self.url+'?m=companies&a=view&company_id=%s&tab=3'%company_id
        response = self.browser.open(url)
        self.content = response.read().decode('utf-8')

    def go_to_all_projects(self):
        self.browser.open(self.url+'?m=projects')
        self.browser.select_form('pickCompany')
        self.browser['department'] = ['company_0']
        response = self.browser.submit()
        self.content = response.read().decode('utf-8')

    def go_to_all_tasks(self):
        self.browser.open(self.url+'?m=tasks')
        self.browser.select_form('taskFilter')
        self.browser['f'] = ['all']
        response = self.browser.submit()
        self.content = response.read().decode('utf-8')

    def go_to_task(self, task_id):
        response = self.browser.open(self.url+'?m=tasks&task_id=%s'%task_id)
        self.content = response.read()
        if is_parent_task(self.content):
            response = self.browser.follow_link(text=PARENT_TAG)
            self.content = response.read()

class AuthenticationException(Exception): pass

