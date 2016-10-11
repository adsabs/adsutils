'''
Created on Dec 6, 2013

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
from adsutils import make_bibcode

class TestBibcodeCreation(unittest.TestCase):

    def test_missing_bibstem(self):
        data = { "year":'2006',
                 "volume":"73",
                 "page":"100407",
                 "author":"'t Hooft",
                 "bibcode":'2006PhRvB..73j0407T',
               }

        self.assertEqual(make_bibcode(data), None)

    def test_apostrophe_author(self):
        data = { "year":'2006',
                 "bibstem":'PhRvB',
                 "volume":"73",
                 "page":"100407",
                 "author":"'t Hooft",
                 "bibcode":'2006PhRvB..73j0407T',
               }

        self.assertEqual(make_bibcode(data), data['bibcode'])

    def test_unicode_author(self):
        data = { "year":"2006",
                 "bibstem":'PhRvB',
                 "volume":"73",
                 "page":"100407",
                 "author":u'\xc0stra',
                 "bibcode":'2006PhRvB..73j0407A',
               }

        self.assertEqual(make_bibcode(data), data['bibcode'])

    def test_entity_author(self):
        data = { "year":"2006",
        "bibstem":'PhRvB',
        "volume":"73",
        "page":"100407",
        "author":"&Ouml;stra",
        "bibcode":'2006PhRvB..73j0407O',
        }

        self.assertEqual(make_bibcode(data), data['bibcode'])

    def test_PhRvL_1(self):
        data = { "year":"2006",
        "bibstem":'PhRvL',
        "volume":"96",
        "page":"255701",
        "author":'Gr&uuml;nwald, Michael',
        "bibcode":'2006PhRvL..96y5701G',
        }

        self.assertEqual(make_bibcode(data), data['bibcode'])

    def test_PhRvL_2(self):
        data = { "year":"2006",
        "bibstem":'PhRvL',
        "volume":"96",
        "page":"295701",
        "author":'Gr&uuml;nwald, Michael',
        "bibcode":'2006PhRvL..96C5701G',
        }

        self.assertEqual(make_bibcode(data), data['bibcode'])

    def test_JGR(self):
        data = { "year":"2007",
        "bibstem":'JGR..',
        "volume":"112",
        "page":'B06410',
        "author":'V',
        "bibcode":'2007JGRB..11206410V',
        }

        self.assertEqual(make_bibcode(data), data['bibcode'])

    def test_WRR(self):
        data = { "year":"2005",
        "bibstem":'WRR..',
        "volume":"41",
        "page":'W11403',
        "author":'Pool, D. R.',
        "bibcode":'2005WRR....4111403P',
        }

        self.assertEqual(make_bibcode(data), data['bibcode'])

    def test_PhT(self):
        data = { "year":"1985",
        "bibstem":'PhT..',
        "volume":"38",
        "issue":"3", 
        "page":"55",
        "author":'Goodwin',
        "bibcode":'1985PhT....38c..55G',
        }

        self.assertEqual(make_bibcode(data), data['bibcode'])

    def test_JHEP(self):
        data = { "year":"2005",
        "bibstem":'JHEP.',
        "volume":"9",
        "page":"5",
        "author":'Boh',
        "bibcode":'2005JHEP...09..005B',
        }

        self.assertEqual(make_bibcode(data), data['bibcode'])

    def test_JOptA(self):
        data = { "year":"2000",
        "bibstem":'JOptA',
        "volume":"2",
        "page":'R1',
        "author":'K',
        "bibcode":'2000JOptA...2R...1K',
        }

        self.assertEqual(make_bibcode(data), data['bibcode'])

    def test_TSTJ(self):
        data = { "year":"2009",
        "bibstem":'TSTJ',
        "volume":"1",
        "page":'08JA03',
        "author":'X',
        "bibcode":'2009TSTJ....1hJA03X',
        }

        self.assertEqual(make_bibcode(data), data['bibcode'])

    def test_praconf(self):
        data = { "year":"2009",
        "bibstem":'pra..conf',
        "page":'E56',
        "author":'S',
        "bibcode":'2009pra..confE..56S',
        }

        self.assertEqual(make_bibcode(data), data['bibcode'])

    def test_OExpr(self):
        data = { "year":"2010",
        "bibstem":'OExpr',
        "volume":"18",
        "issue":'S3',
        "page":'A444',
        "author":'Loser',
        "bibcode":'2010OExpr..18A.444L',
        }

        self.assertEqual(make_bibcode(data), data['bibcode'])

    def test_IJCA(self):
        data = { "year":"2010",
        "bibstem":'IJCA.',
        "volume":"1",
        "issue":"28",
        "page":"127",
        "author":'Cool',
        "bibcode":'2010IJCA....1B.127C',
        }

        self.assertEqual(make_bibcode(data), data['bibcode'])

    def test_PhRB_missing_year_author(self):
        data = { "year":'....',
        "bibstem":'PhRvB',
        "volume":"73",
        "page":"100407",
        "bibcode":'....PhRvB..73j0407.',
        }

        self.assertEqual(make_bibcode(data), None)

    def test_missing_year_author(self):
        data = { "year":'....',
        "bibstem":'JHEP',
        "volume":"1009",
        "page":"31",
        "author":'B',
        "bibcode":'2010JHEP...09..031B',
        }

        self.assertEqual(make_bibcode(data), None)

    def test_SciAm(self):
        data = { "year":"2005",
        "bibstem":'SciAm',
        "volume":"292",
        "page":"36",
        "issue":"3",
        "author":'Lineweaver, C',
        "bibcode":'2005SciAm.292c..36L',
        }

        self.assertEqual(make_bibcode(data), data['bibcode'])

    def test_PLoSO(self):
        data = { "year":"2012",
        "bibstem":'PLoSO',
        "volume":"7",
        "page":'e29977',
        "issue":"1",
        "author":'Takeshi, N',
        "bibcode":'2012PLoSO...729977T',
        }

        self.assertEqual(make_bibcode(data), data['bibcode'])

    def test_PLoSO_2(self):
        data = { "year":"2006",
        "bibstem":'PLoSO',
        "volume":"1",
        "page":'e23',
        "issue":"1",
        "author":'Aboody, Karen',
        "bibcode":'2006PLoSO...1...23A',
        }

        self.assertEqual(make_bibcode(data), data['bibcode'])

    def test_RSPTA(self):
        data = { "year":"2013",
          "bibstem":'RSPTA',
        "volume":"371",
        "page":"20120187",
        "author":'X',
        "bibcode":'2013RSPTA.37120187X',
        }

        self.assertEqual(make_bibcode(data), data['bibcode'])

    def test_PASA(self):
        data = { "year":"2013",
        "bibstem":'PASA.',
        "volume":"30",
        "page":'e003',
        "author":'Dummy',
          "bibcode":'2013PASA...30....3D',
        }

        self.assertEqual(make_bibcode(data), data['bibcode'])

    def test_AMPC(self):
        data = { "year":"2013",
        "bibstem":'AMPC',
        "volume":'03',
        "page":'146',
        "author":'Boudali',
        "bibcode":'2013AMPC....3..146B',
        }

        self.assertEqual(make_bibcode(data), data['bibcode'])
