import sys
import os
import os.path
import time
import unittest2 as unittest
import subprocess
import atexit
import signal

from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.core.management import execute_manager, execute_from_command_line
from splinter.browser import Browser

import settings
from register.models import Task, Project, Employee, Organization, WorkingPeriod

class ModelTestCase(unittest.TestCase):

    def __init__(self, methodName='runTest'):
        unittest.TestCase.__init__(self, methodName)

    def tearDown(self):
        clear_database()

class SplinterTestCase(ModelTestCase):

    def __init__(self, methodName='runTest'):
        ModelTestCase.__init__(self, methodName)
        self.port = '32198'
        self.home = 'http://localhost:%s/netunong' % self.port
        self.process = None

    def setUp(self):
        self.process = self.start_netuno_ng()
        self.browser = Browser()

    def tearDown(self):
        self.browser.quit()
        self.process.terminate()
        self.process.kill()

    def start_netuno_ng(self):
        stdout = stderr = open('netunong.log', 'w')
        argv = [
            os.path.join(os.getcwd(), 'manage.py'), 'runserver', self.port,
        ]
        process = subprocess.Popen(argv, stdout=stdout, stderr=stderr)
        atexit.register(process.terminate)
        atexit.register(process.kill)
        return process
        

def get_organization():
    organization = Organization(name="SEA Tecnologia",
            description="Criadora do Netuno Nova Geracao (NetunoNG)")
    organization.save()
    return organization

def get_organization_project(organization=None):
    if not organization:
        organization = get_organization()
    project = Project(organization=organization, name="NetunoNG", 
                description="Netuno Nova Geracao (NetunoNG)")
    project.save()
    return organization, project

def get_organization_project_task(organization=None, project=None):
    if not organization:
        organization = get_organization()
    if not project:
        _, project = get_organization_project(organization)
    task = Task(name="Test employee", project=project, 
            description="Testing the Employee model")
    task.save()
    return organization, project, task

def get_employee(organization=None, username="test", password="test", task=None):
    if organization is None: organization = get_organization()
    employee = Employee.create_employee(organization=organization,
            username=username, first_name="Test", last_name="Testein",
            middle_name="Testos", email="test@test.tst", password=password)
    if task:
        employee.tasks.add(task) 
    employee.save()
    return employee

def clear_database():
    for model in WorkingPeriod, Task, Project, User, Employee, Organization:
        for instance in model.objects.all():
            instance.delete()
