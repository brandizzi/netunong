import unittest2 as unittest
from employee import employeeTestSuite
from task import taskTestSuite
from working_period import workingPeriodTestSuite

from selenium.login import seleniumLoginTestSuite

try:
    import os
    run_selenium = os.environ['RUN_SELENIUM'] == 'true'
except KeyError:
    run_selenium = False

def suite():
    s = unittest.TestSuite()
    s.addTest(employeeTestSuite)
    s.addTest(workingPeriodTestSuite)
    s.addTest(taskTestSuite)

    if run_selenium:
        s.addTest(seleniumLoginTestSuite)
    
    return s


