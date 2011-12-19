# -*- coding: utf-8 -*-
import os
from cStringIO import StringIO

#from twill import commands, get_browser, set_output
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

    def logout(self):
        response = self.browser.open(self.url+'/index.php?logout=-1')
        self.content = response.read().decode('utf-8')
        if 'loginform' in self.content:
            self.logged_in = False

    def go_to_all_companies(self):
        self.browser.open(self.url)
        link = next(self.browser.links(text_regex='Empresas'))
        response = self.browser.follow_link(link)
        self.browser.select_form('searchform')
        self.browser['owner_filter_id'] = ['0']
        response = self.browser.submit()
        self.content = response.read().decode('utf-8')

    def go_to_users_from_company(self, company_id):
        url = self.url+'?m=companies&a=view&company_id=%s&tab=3'%company_id
        response = self.browser.open(url)
        self.content = response.read().decode('utf-8')
        
