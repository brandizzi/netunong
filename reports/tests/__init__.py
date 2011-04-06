import unittest2 as unittest
from contract import contractTestSuite
from pjcontract import pjContractTestSuite

def suite():
    s = unittest.TestSuite()
    s.addTest(contractTestSuite)    
    s.addTest(pjContractTestSuite)
    return s


