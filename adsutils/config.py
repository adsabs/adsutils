import os

_basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class AppConfig(object):

    DATA_DIR         = '%s/adsutils/data' % _basedir
    UNICODE_DATA     = 'unicode.dat'
    NEEDS_ISSUE      = 'needs_issue.dat'
    IOP_ELECTR       = 'iop_elec.dat'

    RESCLIENT_VERSION= '1.0'
    USER_NAME        = ''
    RESOLVER_URL     = 'http://adsres.cfa.harvard.edu/cgi-bin/refcgi.py'
    LEVEL_MAPPING    = {'0':'Failed','1':'Success','2':'Success','3':'Success','4':'Success','5':'Not verified'}
    URL_MAX          = 4096

    SOURCE_DATA      = ['journals.dat',
                        'journals_abbrev.dat',
                        'conferences.dat',
                        'conferences_abbrev.dat',
                        'preprints.dat',
                        'aps_abbrev.dat',
                        'bibstems.dat' ]
try:
    from local_config import LocalConfig
except ImportError:
    LocalConfig = type('LocalConfig', (object,), dict())

for attr in filter(lambda x: not x.startswith('__'), dir(LocalConfig)):
    setattr(AppConfig, attr, LocalConfig.__dict__[attr])

config = AppConfig
