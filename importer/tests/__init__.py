import unittest2 as unittest

import parser
import organization

def suite():
    s = unittest.TestSuite()
    s.addTest(parser.testSuite)
    s.addTest(organization.testSuite)
    return s


