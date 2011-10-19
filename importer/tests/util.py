import os.path

import unittest2 as unittest
from importer.models import ImportedEntity
from register.models import Organization, Project, Task

SAMPLES_DIR = os.path.join(os.path.dirname(__file__), 'samples')

class ParserTestCase(unittest.TestCase):
    def __init__(self, s):
        unittest.TestCase.__init__(self, s)

    def get_sample_content(self, sample_file):
        return open(os.path.join(SAMPLES_DIR, sample_file)).read()

class ImportedEntityTestCase(unittest.TestCase):
    def __init__(self, s):
        unittest.TestCase.__init__(self, s)

    def setUp(self):
        for model in [ImportedEntity, Organization, Project, Task]:
            model.objects.all().delete()
