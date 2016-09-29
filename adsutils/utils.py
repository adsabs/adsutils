import re
import sys
import socket
import requests
import simplejson as json
from config import config
from .errors import *
# Helper functions for bibcode creation
eIDpat = re.compile(r'^(\d{2})(\w{4})$')

def iopelect_page(p):
    return p.rjust(3,'0').rjust(5,'.')

def jgr_page(s,p):
    page = p[1:]
    qual = p[0]
    if s == 'JGR..' and qual in map(chr, range(65, 72)):
        slist = list(s)
        slist[3] = qual
        s = ''.join(slist)
    else:
        sys.stderr.write('Warning! mismatch for bibstem %s and "CiteID" %s\n'%(s,p))
    return s, page

def bib_page(p):
    # p either has the format 'issue:page' or 'page'
    p = p.replace(' ','')
    qual = ''
    letq = ''
    try:
        issue,page = p.split(':')
        if int(issue) < 1:
            sys.sterr.write('Warning! Page %s has an invalid issue in it (ignored)!\n'%p)
        elif int(issue) < 27:
            qual = chr(96 + int(issue))
        elif int(issue) < 53:
            qual = chr(38 + int(issue))
        else:
            sys.sterr.write('Warning! Page %s has an invalid issue in it (ignored)!\n'%p)
    except:
        page = p
    eIDmat = eIDpat.search(page)
    if eIDmat:
        qual = '.'
        issue = eIDmat.group(1)
        pg  = eIDmat.group(2)
        if int(issue) < 1:
            sys.stderr.write('Warning! Page %s corresponds to issue %s; page formatting is likely wrong!\n' % (page, issue))
        elif int(issue) > 52:
            # this one is pretty hopeless
            sys.stderr.write('Warning! Page %s corresponds to issue %s; page formatting is likely wrong!\n' % (page, issue))
        elif int(issue) > 26:
            # use capital letters in qualifier position
            qual = chr(38 + int(issue))
            sys.stderr.write('Warning! Page %s corresponds to issue %s (%s); page formatting is likely wrong!\n' % (page, issue, qual))
        else:
            # use lower case letters in qualifier position
            qual = chr(96 + int(issue))
        if pg.isdigit():
            pg.rjust(4,'0')
        return "%s%s" % (qual,pg)
    elif is_roman(page):
        # roman numerals are marked by a "D" in 14th column
        page = is_roman(page)
        if int(page) > 0:
            sys.stderr.write('Converted roman numeral %s to page %s\n' % (p,page))
        else:
            page = 0
            sys.stderr.write('Error converting roman numeral page %s\n' % p)
        letq = 'D'
    elif has_page_chars(page):
        cmat = has_page_chars(page)
        page = cmat.group(2)
        letq = cmat.group(1).upper() or cmat.group(3).upper()

    if re.search('\D',page):
        sys.stderr.write('Warning! deleted non-digits from page "%s"\n'%page)
        page = re.sub('\D','',page)

    if page:
        page = page.rjust(5)
    # 2/7/13 -- per Carolyn's request:
    # RSPTA and RSPSA have funky page numbers starting 2013.
    # Can you tweak the bibcode module to "fix" them -
    # I think we should chop the first 3 digits off, unless you have a better idea...
        if len(page) > 5:
            sys.stderr.write('Warning! Trimming page "%s" to last 5 characters\n'%page)
            page = page[-5:]
        page = page.replace(' ','.')
    else:
        page = '.....'
    if qual and letq:
        sys.stderr.write('Warning! found both issue and letter qualifiers, ignoring issue\n')
        qual = ''
    if qual:
        page = re.sub('^.',qual,page)
    if letq:
        page = re.sub('^.',letq,page)

    return page

def is_roman(input):
    input = input.upper(  )
    nums = {'M':1000, 'D':500, 'C':100, 'L':50, 'X':10, 'V':5, 'I':1}
    sum = 0
    for i in range(len(input)):
        try:
            value = nums[input[i]]
            # If the next place holds a larger number, this value is negative
            if i+1 < len(input) and nums[input[i+1]] > value:
                sum -= value
            else: sum += value
        except:
            return False
    # easiest test for validity...
    if to_roman(sum) == input:
        return sum
    else:
        return False

def to_roman(input):
    map = [
        (1000, 'M'),
        (900, 'CM'),
        (500, 'D'),
        (400, 'CD'),
        (100, 'C'),
        (90, 'XC'),
        (50, 'L'),
        (40, 'XL'),
        (10, 'X'),
        (9, 'IX'),
        (5, 'V'),
        (4, 'IV'),
        (1, 'I'),
    ]

    roman_string = ""
    for value, name in map:
        while (value <= n):
            roman_string += name
            n -= value
    return roman_string

def has_page_chars(input):
# these characters are recognized as belonging in 14th column
# if they appear before the page number (see Bibcode)
    page_prechars = "a-prsA-PRS";
    page_postchars = "Pp";
    char_pat = re.compile(r'([%s]?)\s*(\d+)\s*([%s]?)'%(page_prechars, page_postchars))
    return char_pat.search(input)

def get_data(dir,datafile):
	return open("%s/%s"%(dir,datafile)).read().strip().split('\n')

# Machinery for reference resolving
RE_RESULTS = re.compile(r'<li>(?P<bibcode>.{19})\s\(confidence\s(?P<confidence>\d)\)\sfrom\s(?P<refstring>.*?)</li>', re.DOTALL | re.VERBOSE | re.IGNORECASE)

class Resolver:
    def __init__(self):
        self.resolverURL = config.RESOLVER_URL
        self.maxURLlength= config.URL_MAX
        self.LevelMapping= config.LEVEL_MAPPING
        user = "%s@%s" % (config.USER_NAME or 'anonymous', socket.gethostname())
        self.headers = {
                         'User-Agent': 'ADS Reference Resolver Python Client version %s; %s'%(config.RESCLIENT_VERSION,user),
                         'From': '%s' % user,
                         'Content-Type':'application/x-www-form-urlencoded'
                       }
        self.params = {}

    def resolve(self,refdata):
        self.results = []
        if not refdata:
            """
            Really? You called us without given anything to work on?
            """
            raise NoReferenceDataSupplied
        if isinstance(refdata,str):
            """
            This is either one string, or a newline-separated list
            """
            reflist = refdata.split('\n')
        elif isinstance(refdata,list):
            """
            In case of a list of reference strings, there's nothing to be done
            """
            reflist = refdata
        else:
            """
            We don't accept any other formats
            """
            raise InvalidReferenceDataSupplied
        # Fire off the requests to the reference resolver service
        for ref in reflist:
            self.params['resolvethose'] = ref
            self.headers['Content-Length'] = str(len(self.params['resolvethose']))
            try:
                r = requests.post(self.resolverURL, data=self.params, headers=self.headers)
            except:
                raise ResolveRequestFailed
        # Parse the response and return the results as a list of dictionaries
            self.results += self.__parse_results(r.text.strip())

    def __parse_results(self,results):
        """
        The resolve server responds with some basic HTML formatting, where the actual
        results are listed as an HTML list. The regular expression RE_RESULT captures
        each entry
        """
        reslist = []
        cursor = 0
        match  = RE_RESULTS.search(results,cursor)
        while match:
            doc = {}
            doc['bibcode'] = match.group('bibcode')
            doc['confidence'] = self.__get_confidence_level(match.group('confidence'))
            doc['refstring'] = match.group('refstring')
            reslist.append(doc)
            cursor = match.end()
            match  = RE_RESULTS.search(results,cursor)
        return reslist

    def __get_confidence_level(self,level):
        """
        In essence the resolver confidence levels in the range [0,1,2,3,4,5]. In the case
        of '0' the resolver really couldn't make anything from the reference string. Sometimes
        the resolver comes up with a bibcode, either because the journal string found matches
        an known journal close enough, or because the record simply isn't in the ADS. In those
        cases a '5' is assigned. Be very careful with these bibcodes! All other cases are 
        considered as success.
        """
        return self.LevelMapping[level]
            
            
        
