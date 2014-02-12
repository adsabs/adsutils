"""
This module contains source matchers, i.e. classes that receive a string
and return a bibcode it believes should be a bibstem for that string.
"""

import os, sys, re
from config import config
import newtrigdict as newtrigdict

class Error(Exception):
    pass


class SourceMatcher:
    """This is an abstract base class for all source matchers that just
    shows what methods should be implemented.  All getXXX methods return
    lists of bibstems, because it is (unfortunately) well possible that
    two different publications have a common title.
    """
    def __init__(self):
        raise Error, "Can't instanciate SourceMatcher, only children"

    def getExactMatch(self, sourceSpec):
        """Returns a list of bibstems if sourceSpec matches an entry
        in self's data exatly, None otherwise.
        """
        raise Error, "getExactMatch not implemented for this SourceMatcher"

    def getBestMatches(self, sourceSpec, numBest):
        """returns the up to numBest best matches for sourceSpec in a
        list of tuples (score, bibstem).  Doubles may be present, and
        no order should be assumed.
        """
        raise Error, "getBestMatches not implemented for this SourceMatcher"

    def isConfStem(self, stem):
        """returns True if we believe stem belongs to a conference.  It
        doesn't really belong here, but since the only information
        source of this is the files that are used to build a SourceMatcher,
        we're handling it here, anyway.
        """
        raise Error, "isConfStem not implemented for this SourceMatcher"

    def __getitem__(self, sourceSpec):
        """returns a list of (score, bibstem) for the best match for sourceSpec
        """
        raise Error, "__getitem__ not implemented for this SourceMatcher"


class TrigdictSourceMatcher(SourceMatcher):
    """This class implements a SourceMatcher using a combined trigram and
    Levenshtein string edit distance ranking.  It may be instantiated
    with a list of paths to the authority files.  These have to follow
    to be in the format
    <ignored>\\n(<authline>\\n)+
    with <authline> either
    <bibstem>\\t<pubType>\\t<source name>
    or
    <bibstem>\\t<source name>

    PubType is a char specifying that the bibstem refers to a conference (C) or
    to something else (R, J).  If files in the second format are given,
    bibstems in them are assumed to be conferences if the string
    "conferences" appears in their file name.
    """
    def __init__(self, authorityFiles=None):
        if authorityFiles is not None:
            self.authorityFiles = authorityFiles
        else:
            self.authorityFiles = [os.path.join(config.DATA_DIR, s)
                    for s in config.SOURCE_DATA]
        self.bibstemWords = {}
        self._loadSources()

    def _addPub(self, stem, source):
        """Enters stem as value for source.
        """
        key = re.sub("[^A-Za-z0-9&]+", " ", source).strip().upper()
        self.sourceDict[key] = stem
        self.bibstemWords.setdefault(stem, set()).update(
            key.lower().split())

    def _loadTwoPartSource(self, sourceFName, sourceLines):
        """is a helper for _loadOneSource.
        """
        lineno = 1
        enterInConfstems = 0
        if sourceFName.find("conferences")!=-1:
            enterInConfstems = 1
        for ln in sourceLines:
            lineno += 1
            try:
                stem, source = ln.split("\t", 1)
                stem = stem.strip()[-9:]
                if not source.strip():
                    sys.stderr.write("sourcematchers.py: warning: skipping entry %s in file %s\n"%(ln.strip(),sourceFName))
                    continue
                self._addPub(stem, source)
                if enterInConfstems:
                    self.confstems[stem] = 1
            except ValueError:
                sys.stderr.write("sourcematchers.py: %s (%d): skipping source line: %s"%(sourceFName,lineno,ln))

    def _loadThreePartSource(self, sourceFName, sourceLines):
        """is a helper for _loadOneSource.
        """
        lineno = 1
        for ln in sourceLines:
            lineno += 1
            try:
                stem, pubType, source = ln.split("\t", 2)
                stem = stem.strip()[-9:]
                self._addPub(stem, source)
                if pubType=="C":
                    self.confstems[stem] = 1
            except ValueError:
                sys.stderr.write("sourcematchers.py: %s (%d): skipping source line: %s"%(sourceFName,lineno,ln))

    def _loadOneSource(self, sourceFName):
        """handles one authority file including format auto-detection.
        """
        sourceLines = open(sourceFName).readlines()
        del sourceLines[0]
        if len(sourceLines[0].split("\t"))==2:
            self._loadTwoPartSource(sourceFName, sourceLines)
        elif len(sourceLines[0].split("\t"))==3:
            self._loadThreePartSource(sourceFName, sourceLines)
        else:
            raise Error, "%s does not appear to be a source authority file"

    def _loadSources(self):
        """creates a trigdict and populates it with data from self.autorityFiles
        """
        self.confstems = {}
        self.sourceDict = newtrigdict.Trigdict()
        for fName in self.authorityFiles:
            self._loadOneSource(fName)
        # We want to allow naked bibstems in references, too
        for stem in self.sourceDict.values():
            cleanStem = stem.replace(".", "").upper()
            self._addPub(stem, cleanStem)

    def getExactMatch(self, sourceSpec):
        """Returns a bibcode if sourceSpec matches an entry in self's data
        exatly, None otherwise.
        """
        return self.sourceDict.exactmatch(sourceSpec)

    def getBestMatches(self, sourceSpec, numBest):
        """returns the up to numBest best matches for sourceSpec in a
        list of tuples (score, bibstem).  Doubles may be present, and
        no order should be assumed.
        """
        return self.sourceDict.bestmatches(sourceSpec, numBest)

    def isConfStem(self, stem):
        """see SourceMatcher.isConfStem.
        """
        return self.confstems.has_key(stem)

    def __getitem__(self, sourceSpec):
        """returns the (score, bibstem) for the best match for sourceSpec
        """
        return self.sourceDict[sourceSpec]