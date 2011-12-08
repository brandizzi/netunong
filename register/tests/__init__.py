import unittest2 as unittest
from employee import employeeTestSuite
from project import projectTestSuite
from task import taskTestSuite
from working_period import workingPeriodTestSuite

from application import registerAppTestSuite

def suite():
    s = unittest.TestSuite()
    s.addTest(employeeTestSuite)
    s.addTest(workingPeriodTestSuite)
    s.addTest(taskTestSuite)
    s.addTest(projectTestSuite)
    s.addTest(registerAppTestSuite)
    return s


