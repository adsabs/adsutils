"""
this module implements a class that works like a dictionary, only that
the keys are trigram-searched and then levenshtein-weighted.
A getitem returns sorted list [(score,value), ...]
"""

import sys
import ctrigram as ctrigram

globallock = 0

class Trigdict:
    """You could use it like this:
    >>> d = Trigdict()
    >>> d["KL"], d["KLOM"], d["KLOM"] = "Short", "Hallo", "Second"
    >>> d["AKLOM"], d["PKLOP"], d["PKLOA"] = "Hillo", "Hullo", "pHullo"
    >>> d["KL"]
    [(1, 'Short')]
    >>> d["KLOM"]
    [(1.0, 'Second'), (1.0, 'Hallo')]
    >>> str(d.bestmatches("KLOMA", 3))[:60]
    "[(0.75999999046325684, 'Hillo'), (0.87999999523162842, 'Seco"
    >>> d["PKLOOO"]
    [(0.77777779102325439, 'pHullo')]
    """
    def __init__(self):
        global globallock
        if globallock:
            sys.stderr.write("Only one trigdict allowed with ctrigram.  Bye.\n")
            sys.exit(1)
        globallock = 1
        self.allKeys = set()
        self.allValues = set()
        self.valdict = {}
        self.recreatedict = 1
        self.lock = 0
        self.shortdict = {}

    def makedict(self):
        if self.lock:
            sys.stderr.write("Cannot recreate dictionary with ctrigram.  Bye.\n")
            sys.exit(1)
        ctrigram.buildindex([w for w in self.allKeys])
        self.lock = 1
        self.recreatedict = 0

    def     __setitem__(self, source, val):
        self.allKeys.add(source)
        self.allValues.add(val)
        if len(source)<3:
            self.shortdict.setdefault(source, []).append(val)
        self.valdict.setdefault(source, []).append(val)
        self.recreatedict = 1

    def exactmatch(self, source):
        if self.valdict.has_key(source):
            return [(1, b) for b in self.valdict[source]]
        else:
            return None

    def __getitem__(self, source, numitem=1):
        if self.recreatedict:
            self.makedict()
        matchlist = []
        matchdict = {}
        if len(source)<3:
            return [(1, w) for w in self.shortdict.get(source, [])]
        candidateMatches = ctrigram.lookup(source, numitem)
        if candidateMatches is None:
            return []
        res = []
        for matSource, score in candidateMatches[:numitem]:
            for stem in self.valdict[matSource]:
                res.append((score, stem))
        res.reverse()
        return res

    def bestmatches(self, word, numitem):
        return self.__getitem__(word, numitem)

    def keys(self):
        return self.allKeys

    def values(self):
        return self.allValues

def _test():
    import doctest, newtrigdict
    return doctest.testmod(newtrigdict)

if __name__=="__main__":
    _test()
