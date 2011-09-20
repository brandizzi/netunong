import unittest2 as unittest

import parser

def suite():
    s = unittest.TestSuite()
    s.addTest(parser.testSuite)
    return s


