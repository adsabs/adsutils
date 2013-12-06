import os

_basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class AppConfig(object):

    DATA_DIR         = '%s/data' % _basedir
    UNICODE_DATA     = 'unicode.dat'
    NEEDS_ISSUE      = 'needs_issue.dat'
    IOP_ELECTR       = 'iop_elec.dat'

try:
    from local_config import LocalConfig
except ImportError:
    LocalConfig = type('LocalConfig', (object,), dict())

for attr in filter(lambda x: not x.startswith('__'), dir(LocalConfig)):
    setattr(AppConfig, attr, LocalConfig.__dict__[attr])

config = AppConfig
