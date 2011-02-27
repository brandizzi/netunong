import unittest2 as unittest
from employee import employeeTestSuite
from task import taskTestSuite
from working_period import workingPeriodTestSuite

def suite():
    s = unittest.TestSuite()
    s.addTest(employeeTestSuite)
    s.addTest(workingPeriodTestSuite)
    s.addTest(taskTestSuite)
    return s


