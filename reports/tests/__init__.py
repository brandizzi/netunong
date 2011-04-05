import unittest2 as unittest
from contract import contractTestSuite

def suite():
    s = unittest.TestSuite()
    s.addTest(contractTestSuite)    
    return s


