#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import re
import sys
import string
from UserDict import UserDict

RE_HEX = re.compile('^[0-9a-fA-F]+$')

# Courtesy of Chase Seibert.
# http://bitkickers.blogspot.com/2011/05/stripping-control-characters-in-python.html
RE_XML_ILLEGAL = u'([\u0000-\u0008\u000b-\u000c\u000e-\u001f\ufffe-\uffff])' + \
                 u'|' + \
                 u'([%s-%s][^%s-%s])|([^%s-%s][%s-%s])|([%s-%s]$)|(^[%s-%s])' % \
                  (unichr(0xd800),unichr(0xdbff),unichr(0xdc00),unichr(0xdfff),
                   unichr(0xd800),unichr(0xdbff),unichr(0xdc00),unichr(0xdfff),
                   unichr(0xd800),unichr(0xdbff),unichr(0xdc00),unichr(0xdfff),
                   )

class UnicodeHandlerError(Exception):
    """
    Error in the UnicodeHandler.
    """
    pass

class UnicodeHandler(UserDict):
    """Loads a table of Unicode Data from a file.

Each line of the file consists in 4 or 5 fields.
Field description:
1/ Unicode code
2/ Entity name
3/ Ascii representation
4/ Latex representation
5/ Type (optional) can be P=ponctuation, S=space, L=lowercase-letter, U=uppercase-letter

"""

    re_entity = re.compile('&([a-zA-Z0-9]{2,}?);')
    re_numentity = re.compile('&#(?P<number>\d+);')
    re_hexnumentity = re.compile('&#x(?P<hexnum>[0-9a-fA-F]+);')

    #re_unicode = re.compile(u'([\u0080-\uffff])')
    re_unicode = re.compile(r'\\u(?P<number>[0-9a-fA-F]{4})')

    # accents with a slash in front. To be converted to entities
    accents = {
                   "'": 'acute',
                   "`": "grave",
                   "^": "circ"
                 }

    re_accent = re.compile(r'([aeiouAEIOU])\\([\%s])' %
                            '\\'.join(accents.keys()))

    # entities that should be combined with previous character
    missent = {
                  'acute'  : 'acute',
                  'grave'  : 'grave',
                  'caron'  : 'caron',
                  'circ'   : 'circ',
                  'uml'    : 'uml',
                  '#x00b4' : 'acute',
                  '#x00b8' : 'cedil',
                  '#x2041' : 'circ',
                  '#x00af' : 'macron',
                 }

    re_missent = re.compile(r'([a-zA-Z])&(%s);' % '|'.join(missent.keys()))
    re_missent_space = re.compile(r'([\s\;])&(%s);' % '|'.join(missent.keys()))

    # some entities not in entities table. Maybe not acurate: aproximation
    morenum = {
                  '#x030a': '',
                  '#x01ce': 'acaron',
                  '#x01d0': 'icaron',
                  '#x01e7': 'gcaron',
                  '#x0229': 'ecedil',
                  '#x025b': 'epsilon',
                  '#x1e21': 'gmacron',
                  '#x030b': '',
                  '#x1ed3': 'ocirc',
                  '#x0317': '',
                  '#x03d2': 'Upsilon',
                  '#x00fd': 'yacute'
                 }
    re_morenum = re.compile(r'&(%s);' % '|'.join(morenum.keys()))

    def __init__(self,file):

        self.file = file
        self.unicode = [None,] * 65536

        try:
            lines = open(self.file).readlines()
        except IOError:
            sys.stderr.write("ads.Unicode: Warning: annot open Unicode Table file %s\n" % self.file)
            raise IOError,"Cannot open Unicode Table "+self.file
        else:
            UserDict.__init__(self)
            for line in lines:
                fields = line.split()
                fields = [ field.replace('"','') for field in fields ]

                if len(fields) > 3:
                    try:
                        code = int(fields[0].split(':')[0].split(';')[0])
                        entity = fields[1]
                        self[entity] = UnicodeChar(fields)  # keep entity table

                        if len(fields) > 4:    # keep code table
                            if not self.unicode[code]:
                                self.unicode[code] = self[entity]
                            else:
                                pass
                    except ValueError:
                        pass

    def getUnicode(self,ucode):
        code = ord(ucode)
        if self.unicode[code]:
            return self.unicode[code]

    def ent2nument(self,str):
        retstr = self.re_entity.sub(self.__sub_num_entity,str)
        return retstr

    def ent2asc(self,str):
        str = re.sub('__amp__','&',str)
        retstr = self.re_entity.sub(self.__sub_asc_entity,str)
        retstr = self.re_numentity.sub(self.__sub_numasc_entity,retstr)
        retstr = self.re_hexnumentity.sub(self.__sub_hexnumasc_entity,retstr)
        return retstr

    def ent2u(self,str):
        retstr = self.re_entity.sub(self.__sub_entity, str)
        retstr = self.re_numentity.sub(self.__numeric_entity_to_unicode, retstr)
        retstr = self.re_hexnumentity.sub(self.__hexadecimal_entity_to_unicode, retstr)
        return retstr

    def u2asc(self,str):
        retstr = re.sub(r'\-unknown\-entity\-(.)([^\-]+)\-','\g<1>',str)
        retstr = ''.join([self.__toascii(char) for char in retstr ])
        return retstr

    def u2ent(self,str):
        retstr = re.sub(r'\-unknown\-entity\-([^\-]+)\-','&\g<1>;',str)
        retstr = ''.join([self.__toentity(char) for char in retstr ])
        retstr = self.re_unicode.sub(self.__sub_hexnum_toent,retstr)
        return retstr

    def encode(self,str):
        data = self.u2ent(str)
        data = data.replace("&", "&amp;")
        data = data.replace("<", "&lt;")
        data = data.replace("\"", "&quot;")
        data = data.replace(">", "&gt;")
        return data

    def remove_control_chars(self, input):
        input = re.sub(RE_XML_ILLEGAL, "", input)
        input = re.sub(r"[\x01-\x1F\x7F]", "", input)
        return input

    def cleanall(self,str,cleanslash=0):
        """Deals with things like:
1./ accents with a slashes and converts them to entities.
Example: \', \`,\^

2./ Some 'missed' incomplete entities or &#x00b4; ( floating apostroph )
and the like.
Example: Milos&caron;evic -->  Milo&scaron;evic
        Marti&#00b4;nez  -->  Mart&iacute;nez

3./ Get rid of remaining numeric entities.
Converts them from an aproximation table or set to unknown.

4./ If option 'cleanslash' is set takes 'dangerous' radical action with
slashes. Gets rid of all of them. Also converts 'l/a' to '&lstrok;a'. Maybe cases
in which this is substituting too much?
"""
        retstr = self.re_accent.sub(self.__sub_accent,str)
        retstr = self.re_missent.sub(self.__sub_missent,retstr)
#         retstr = self.re_missent_space.sub('',retstr)
        retstr = self.re_morenum.sub(self.__sub_morenum,retstr)
        # 11/5/02 AA - add translation of &rsquo; and &rsquor; into
        #              single quote character
        retstr = re.sub(r'&rsquor?;',"'",retstr)
        if cleanslash:
            retstr = re.sub(r'\\','',retstr)
            retstr = re.sub(r'([Ll])/','&\g<1>strok;',retstr)
        return retstr

    def __sub_accent(self,match):
        return "&%s%s;" % (match.group(1), self.accents[match.group(2)])

    def __sub_missent(self,match):
        ent = "%s%s" % (match.group(1), self.missent[match.group(2)])
        if ent in self.keys():
            return "&%s;" % ent
        else:
            return "%s&%s;" % (match.group(1), self.missent[match.group(2)])

    def __sub_morenum(self,match):
        return "&%s;" % (self.morenum[match.group(1)])

    def __sub_entity(self,mat):
        ent = mat.group(1)
        if ent in self.keys():
            ret = eval("u'\\u%04x'" % self[ent].code)
            return ret
        else:
            raise UnicodeHandlerError('Unknown numeric entity: %s' % mat.group(0))

    def __sub_num_entity(self,mat):
        ent = mat.group(1)
        if ent in self.keys():
            ret = "&#x%04x;" % self[ent].code
            return ret
        else:
            raise UnicodeHandlerError('Unknown hexadecimal entity: %s' % mat.group(0))

    def __sub_numasc_entity(self,mat):

        entno = int(mat.group('number'))

        try:
            if self.unicode[entno]:
                return self.unicode[entno].ascii
            elif entno < 255:
                return self.u2asc(chr(entno))
        except IndexError:
            raise UnicodeHandlerError('Unknown numeric entity: %s' % mat.group(0))

    def __sub_hexnumasc_entity(self,mat):

        entno = int(mat.group('hexnum'),16)
        try:
            if self.unicode[entno]:
                return self.unicode[entno].ascii
            elif entno < 255:
                return self.u2asc(chr(entno))
        except IndexError:
            raise UnicodeHandlerError('Unknown hexadecimal entity: %s' % mat.group(0))

    def __numeric_entity_to_unicode(self, match):

        entity_number = int(match.group('number'))
        try:
            return unichr(entity_number)
        except ValueError:
            raise UnicodeHandlerError('Unknown numeric entity: %s' % match.group(0))

    def __hexadecimal_entity_to_unicode(self, match):

        entity_number = int(match.group('hexnum'), 16)
        try:
            return unichr(entity_number)
        except ValueError:
            raise UnicodeHandlerError('Unknown hexadecimal entity: %s' % match.group(0))

    def __sub_hexnum_toent(self,mat):

        try:
            entno = int(mat.group('number'),16)
        except ValueError:
            return r'\u' + mat.group('number')

        if self.unicode[entno]:
            return '&%s;' % self.unicode[entno].entity
        else:
            raise UnicodeHandlerError('Unknown hexadecimal entity: %s' % entno)

    def __sub_asc_entity(self,mat):
        ent = mat.group(1)
        if ent in self.keys():
            ret = self[ent].ascii
            return ret
        else:
            raise UnicodeHandlerError('Unknown named entity: %s' % mat.group(0))

    def __toascii(self,char):
        nchar = ord(char)

        if nchar <= 128:
            return char

        if self.unicode[nchar]:
            return self.unicode[nchar].ascii
        else:
            raise UnicodeHandlerError('Unknown character code: %d' % nchar)

    def __toentity(self, char):
        nchar = ord(char)

        if nchar <= 128:
            # Return the ASCII characters.
            return char

        if self.unicode[nchar] is not None:
            # We have a named entity.
            return '&%s;' % self.unicode[nchar].entity
        else:
            # Return a numeric entity.
            return '&#%d;' % nchar

    def __str__(self):
        return str(self.keys())

class UnicodeChar:
    def __init__(self,fieldlist):
        self.code = int(fieldlist[0].strip())
        self.entity = fieldlist[1].strip()
        self.ascii = fieldlist[2].strip()
        self.latex = fieldlist[3].strip()
        if len(fieldlist) > 4:
            self.type = fieldlist[4].strip()
        else:
            self.type = ''

    def __str__(self):
        return self.ascii
