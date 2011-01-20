import unittest
from test.employee import employeeTestSuite

def suite():
    s = unittest.TestSuite()
    s.addTest(employeeTestSuite)
    return s




