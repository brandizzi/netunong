import unittest
from test.employee import employeeTestSuite
from test.working_period import workingPeriodTestSuite

def suite():
    s = unittest.TestSuite()
    s.addTest(employeeTestSuite)
    s.addTest(workingPeriodTestSuite)
    return s




