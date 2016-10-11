# coding: utf-8
#!/usr/bin/env python
import os
import sys
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

major, minor1, minor2, release, serial =  sys.version_info

readfile_kwargs = {"encoding": "utf-8"} if major >= 3 else {}

def readfile(filename):
    with open(filename, **readfile_kwargs) as fp:
        contents = fp.read()
    return contents

version_regex = re.compile("__version__ = \"(.*?)\"")

contents = readfile(os.path.join(
    os.path.dirname(os.path.abspath('__file__')),
    "adsutils", "__init__.py"))

data_dir = os.path.join(os.path.dirname(os.path.abspath('__file__')),"adsutils","data")

version = version_regex.findall(contents)[0]

setup(
    name = 'adsutils',
    version = version,
    install_requires = ['pip>=1.4.1', 'unittest2', 'nose', 'requests', 'simplejson', 'ads_modules'],
    author = 'Edwin Henneken',
    author_email = 'ehenneken@cfa.harvard.edu',
    url = 'http://github.com/adsabs/adsutils',
    license="MIT",
    description="A Python tool with some general ADS utilities",
    packages = ['adsutils', 'adsutils.test'],
    include_package_data=True,
    package_data={'adsutils': ['adsutils/data/*.dat']},
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Operating System :: POSIX :: Linux',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries'    ]
)
