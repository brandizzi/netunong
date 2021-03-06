import os
import os.path
from glob import glob
from multiprocessing import Process
from netunomock.server import run_server
from time import sleep

import unittest2 as unittest

from django.contrib.auth.models import User

from importer.models import ImportedEntity, ExportedLog
from register.models import Organization, Project, Task, Employee

SAMPLES_DIR = os.path.join(os.path.dirname(__file__), 'samples')
MODELS = [
        ExportedLog, ImportedEntity, Organization, 
        Project, Task, Employee, User
]

def clear_database():
    for model in MODELS:
        model.objects.all().delete()

class ParserTestCase(unittest.TestCase):
    def __init__(self, s):
        unittest.TestCase.__init__(self, s)

    def get_sample_content(self, sample_file):
        return open(os.path.join(SAMPLES_DIR, sample_file)).read()

class ModelTestCase(unittest.TestCase):
    def __init__(self, s):
        unittest.TestCase.__init__(self, s)

    def setUp(self):
        clear_database()
        

class NetunomockTestCase(unittest.TestCase):
    def __init__(self, s):
        unittest.TestCase.__init__(self, s)

    def setUp(self):
        self.server = Process(target=run_server)
        self.server.start()
        sleep(0.5)

    def tearDown(self):
        self.server.terminate()
        for f in glob('importer.*.log'):
            os.remove(f)
