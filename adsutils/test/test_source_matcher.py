'''
Created on Feb 10, 2014

@author: ehenneken
'''

import os
import sys
import site
tests_dir = os.path.dirname(os.path.abspath(__file__))
site.addsitedir(os.path.dirname(tests_dir)) #@UndefinedVariable
site.addsitedir(tests_dir) #@UndefinedVariable

if sys.version_info < (2,7):
    import unittest2 as unittest
else:
    import unittest

from adsutils import get_pub_abbreviation
from adsutils.errors import *

class TestResolver(unittest.TestCase):

    def test_missing_data(self):
        jstring = ''
        self.assertEqual(get_pub_abbreviation(jstring), [])
    
    def test_exact_match_mismatch(self):
        jstring = 'Astrop J'
        self.assertEqual(get_pub_abbreviation(jstring, exact=True), [])
    
    def test_exact_match_match(self):
        jstring = 'Astrophysical Journal'
        self.assertEqual(get_pub_abbreviation(jstring, exact=True), [(1, 'ApJ......')])