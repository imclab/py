"""
    most basic syntx reminder for unit/nose tests
    run w "nosetests -s" from CLI to print to stdout
    
    http://nose.readthedocs.org/en/latest/testing.html
"""

import unittest

class Basics(unittest.TestCase):

    def setUp(self):
        print "setting up..."
        
    def tearDown(self):
        print "tearing down..."
        
    def test_true(self):
        assert True
        
    def test_false(self):
        assert False
    
    