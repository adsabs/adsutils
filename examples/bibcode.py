"""
Example script for how to create bibcodes
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from adsutils import make_bibcode


data = { "year":'2006',
         "bibstem":'PhRvB',
         "volume":"73",
         "page":"100407",
         "author":"'t Hooft",
       }
print "Input data: %s" % str(data)
print "Bibcode: %s\n" % make_bibcode(data)

data = {"year":"2006",
        "bibstem":'PhRvL',
        "volume":"96",
        "page":"295701",
        "author":'Gr&uuml;nwald, Michael',
        }
print "Input data: %s" % str(data)
print "Bibcode: %s\n" % make_bibcode(data)

data = { "year":"2000",
        "bibstem":'JOptA',
        "volume":"2",
        "page":'R1',
        "author":'K',
        "bibcode":'2000JOptA...2R...1K',
        }
print "Input data: %s" % str(data)
print "Bibcode: %s\n" % make_bibcode(data)