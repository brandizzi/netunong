# -*- coding: utf-8 -*-
import os

from twill import commands, get_browser, set_output

def greeting():
    return u'Bem-vind'
    
class NetunoCrawler(object):

    def __init__(self, url):
        set_output(file(os.devnull, 'w'))
        self.logged_in = False
        self.url = url
        self.browser = get_browser()

    def login(self, username, password):
        commands.go(self.url)
        commands.fv('loginform', 'username', username)  
        commands.fv('loginform', 'password', password)      
        commands.submit()
        if greeting() in self.browser.get_html().decode('utf-8'):
            self.logged_in = True

    def logout(self):
        commands.go(self.url+'/index.php?logout=-1')
        if 'loginform' in self.browser.get_html().decode('utf-8'):
            self.logged_in = False
