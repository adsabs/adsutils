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

from config import config
from adsutils import resolve_references
from adsutils.errors import *

class TestResolver(unittest.TestCase):

    def test_missing_data(self):
        refstring = ''
        try:
            self.assertEqual(resolve_references(refstring), data)
        except Exception, e:
            self.assertIsInstance(e, NoReferenceDataSupplied)

    def test_invalid_data(self):
        refstring = {'a':'b'}
        try:
            self.assertEqual(resolve_references(refstring), data)
        except Exception, e:
            self.assertIsInstance(e, InvalidReferenceDataSupplied)

    def test_one_reference(self):
        data = [{'refstring': u'Hermsen, W., et. al. 1992, IAU Circ. No. 5541', 
                'confidence': 'Success', 
                'bibcode': u'1992IAUC.5541....1H'
               }]
        refstring = 'Hermsen, W., et. al. 1992, IAU Circ. No. 5541'
        self.assertEqual(resolve_references(refstring), data)

    def test_multiple_references_list(self):
        data = [{'refstring': u'Abt, H. 1990, ApJ, 357, 1', 
                 'confidence': 'Success', 
                 'bibcode': u'1990ApJ...357....1A'},     
                {'refstring': u'J. B. Gupta, and J. H. Hamilton, Phys. Rev. C 16, 427 (1977)', 
                 'confidence': 'Success', 
                 'bibcode': u'1977PhRvC..16..427G'}, 
                {'refstring': u'Hermsen, W., et. al. 1992, IAU Circ. No. 5541', 
                  'confidence': 'Success', 
                  'bibcode': u'1992IAUC.5541....1H'}, 
                {'refstring': u'Pollock, J. T. 1982, Ph. D. Thesis, University of Florida', 
                 'confidence': 'Success', 
                 'bibcode': u'1982PhDT.........1P'}]
        refdata = ['Abt, H. 1990, ApJ, 357, 1', 
                   'J. B. Gupta, and J. H. Hamilton, Phys. Rev. C 16, 427 (1977)', 
                   'Hermsen, W., et. al. 1992, IAU Circ. No. 5541', 
                   'Pollock, J. T. 1982, Ph. D. Thesis, University of Florida']
        self.assertEqual(resolve_references(refdata), data)

    def test_multiple_references_newline(self):
        data = [{'refstring': u'Abt, H. 1990, ApJ, 357, 1', 
                 'confidence': 'Success', 
                 'bibcode': u'1990ApJ...357....1A'},     
                {'refstring': u'J. B. Gupta, and J. H. Hamilton, Phys. Rev. C 16, 427 (1977)', 
                 'confidence': 'Success', 
                 'bibcode': u'1977PhRvC..16..427G'}, 
                {'refstring': u'Hermsen, W., et. al. 1992, IAU Circ. No. 5541', 
                  'confidence': 'Success', 
                  'bibcode': u'1992IAUC.5541....1H'}, 
                {'refstring': u'Pollock, J. T. 1982, Ph. D. Thesis, University of Florida', 
                 'confidence': 'Success', 
                 'bibcode': u'1982PhDT.........1P'}]
        refdata = "\n".join(['Abt, H. 1990, ApJ, 357, 1', 
                   'J. B. Gupta, and J. H. Hamilton, Phys. Rev. C 16, 427 (1977)', 
                   'Hermsen, W., et. al. 1992, IAU Circ. No. 5541', 
                   'Pollock, J. T. 1982, Ph. D. Thesis, University of Florida'])
        self.assertEqual(resolve_references(refdata), data)