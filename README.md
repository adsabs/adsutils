[![Build Status](https://travis-ci.org/adsabs/adsutils.svg?branch=master)](https://travis-ci.org/adsabs/adsutils)
[![Coverage Status](https://coveralls.io/repos/github/adsabs/adsutils/badge.svg?branch=master)](https://coveralls.io/github/adsabs/adsutils?branch=master)

ADSutils
========

This is a module with various ADS specific utilities

## Installing

Clone the repo to a local directory
```
git clone https://github.com/adsabs/adsutils adsutils 
```
Go into the newly created directory and create a virtual environment
```
virtualenv --no-site-packages -ppython2.7 venv
```
and start it
```
source venv/bin/activate
```
Update `pip` like
```
pip install -U pip
```
and then install the required software
```
pip install -r requirements.txt
```
Test if things are working:
```
python test/nosetests.py
```
## Utility to create bibcodes

Import the relevant module:
```
from adsutils import make_bibcode
```
and provide the necessary metadata:
```
data = {"year":"2006",
        "bibstem":'PhRvL',
        "volume":"96",
        "page":"295701",
        "author":'Gr&uuml;nwald, Michael',
        }
```
and then call
```
bibcode = make_bibcode(data)
```
and a bibcode will get generated. You will have to determine the correct journal abbreviation (bibstem). The journal abbreviations are available here: http://adsabs.harvard.edu/abs_doc/journals2.html

## Utility to resolve reference strings

Import the relevant module:
```
from adsutils import resolve_references
```
You can provide reference data in various formats:
* A single reference string
* A newline-separated set of reference strings
* A (Python) list of reference strings

Examples:
A case with just one reference string:
```
refdata = 'Hermsen, W., et. al. 1992, IAU Circ. No. 5541'
result = resolve_references(refdata)
```
in which case the result (always a list of dictionaries) will look like
```
[{'refstring': u'Hermsen, W., et. al. 1992, IAU Circ. No. 5541', 
 'confidence': 'Success', 
 'bibcode': u'1992IAUC.5541....1H'
}]
```
Multiple reference strings work as follows:
```
refdata = ['J. B. Gupta, and J. H. Hamilton, Phys. Rev. C 16, 427 (1977)', 'Pollock, J. T. 1982, Ph. D. Thesis, University of Florida']
result = resolve_references(refdata)
```
in which case the result (always a list of dictionaries) will look like
```
[{'refstring': u'J. B. Gupta, and J. H. Hamilton, Phys. Rev. C 16, 427 (1977)', 
  'confidence': 'Success', 
  'bibcode': u'1977PhRvC..16..427G'},  
 {'refstring': u'Pollock, J. T. 1982, Ph. D. Thesis, University of Florida', 
  'confidence': 'Success', 
  'bibcode': u'1982PhDT.........1P'}]
```
# Possible outcome
The resolver can return three classes of 'confidence' levels:
* Success
* Failed
* Not verified

The only class that needs some explanation is the last one; it is quite possible that the metadata contains enough information to guess a bibcode. The year could be off by 1 (which can also apply to the page or volume number) or a journal was abbreviated in a non-standard way. It is also possible that all the metadata is correct, but the record is not in the ADS database. Even though a bibcode is returned, you cannot assume it is correct. These <em>Not verified</em> cases need further inspection.

## Utility to get ADS journal abbreviation from publication name

An essential part of the ADS publication identifier (<em>bibcode</em>) is the publication abbreviation (<em>bibstem</em>). This utility takes a string representing the publication name and attempts to match it to an ADS abbreviation. It returns a list of candidates and associated scores.

Import the relevant module:
```
from adsutils import get_pub_abbreviation
```
The bibstem candidates are then found as follows:
```
pubstring = 'American Astronautical Society Meeting'
result = get_pub_abbreviation(pubstring)
```
which returns a list of tuples with candidates and their associated scores (sorted by score, descending):
```
[(1.0, 'aans.meet'), (0.98545706272125244, 'AAS......'), (0.95637118816375732, 'aans.symp'), (0.93698060512542725, 'AAS......'), (0.91897505521774292, 'acs..meet')]
```
You can specify that you are only interested in exact matches in the following way:
```
pubstring = 'Astrophysical Journal'
result = get_pub_abbreviation(pubstring, exact=True)
```
which would result in
```
[(1, 'ApJ......')]
```
while
```
pubstring = 'Astrophysical Journ'
result = get_pub_abbreviation(pubstring, exact=True)
```
would result in
```
[]
```
