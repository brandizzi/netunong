import unittest2 as unittest

import company_parser, project_parser, task_parser, user_parser
import organization, project, task

def suite():
    s = unittest.TestSuite()
    s.addTest(company_parser.testSuite)
    s.addTest(project_parser.testSuite)
    s.addTest(task_parser.testSuite)
    s.addTest(user_parser.testSuite)
    s.addTest(organization.testSuite)
    s.addTest(project.testSuite)
    s.addTest(task.testSuite)
    return s


