import unittest2 as unittest

import company_parser, project_parser
import organization

def suite():
    s = unittest.TestSuite()
    s.addTest(company_parser.testSuite)
    s.addTest(project_parser.testSuite)
    s.addTest(organization.testSuite)
    return s


