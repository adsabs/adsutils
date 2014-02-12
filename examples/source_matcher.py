"""
Example script for how to use the reference resolver
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from adsutils import get_pub_abbreviation
# Try an exact match
pubstring = 'Astrophysical Journ'
print "Trying an exact match for: %s" % pubstring
result = get_pub_abbreviation(pubstring, exact=True)
print "Result: %s" % str(result)
# First we resolve a journal
pubstring = 'Astrophysical Journ'
print "Trying a fuzzy match for: %s" % pubstring
result = get_pub_abbreviation(pubstring)
print "Result: %s" % str(result)
# Next we resolve a conference name
pubstring = 'American Astronautical Society Meeting'
print "Matching: %s" % pubstring
result = get_pub_abbreviation(pubstring)
print "Result: %s" % str(result)
