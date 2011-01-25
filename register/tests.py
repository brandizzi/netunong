import unittest2 as unittest
from test.employee import employeeTestSuite
from test.task import taskTestSuite
from test.working_period import workingPeriodTestSuite

def suite():
    s = unittest.TestSuite()
    s.addTest(employeeTestSuite)
    s.addTest(workingPeriodTestSuite)
    s.addTest(taskTestSuite)
    return s




