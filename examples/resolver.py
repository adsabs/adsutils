"""
Example script for how to use the reference resolver
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from adsutils import resolve_references
# First we resolve a single reference string
refdata = 'Hermsen, W., et. al. 1992, IAU Circ. No. 5541'
print "Resolving: %s" % refdata
result = resolve_references(refdata)
print "Result: %s" % str(result)
# Next we resolve a list of references
refdata = ['Abt, H. 1990, ApJ, 357, 1', 'J. B. Gupta, and J. H. Hamilton, Phys. Rev. C 16, 427 (1977)', 'Hermsen, W., et. al. 1992, IAU Circ. No. 5541', 'Pollock, J. T. 1982, Ph. D. Thesis, University of Florida']
print "Resolving: %s" % str(refdata)
result = resolve_references(refdata)
print "Result: %s" % str(result)
