#!/usr/bin/env python
#encoding: utf8

from __future__ import print_function

import os
import re
import sys

from setuptools import setup
from setuptools import find_packages
from setuptools.command.test import test as TestCommand

try:
    import colorama
    colorama.init()
    from colorama import Fore
    RESET = Fore.RESET
    GREEN = Fore.GREEN
    RED = Fore.RED
except ImportError:
    RESET = ''
    GREEN = ''
    RED = ''

import inspect
from os.path import join, dirname, abspath
OWN_PATH = abspath(inspect.getfile(inspect.currentframe()))
EXAMPLES_DIR = join(dirname(OWN_PATH), 'examples')

v = open(os.path.join(os.path.dirname(__file__), 'ubl', '__init__.py'), 'r')
VERSION = re.match(r".*__version__ = '(.*?)'", v.read(), re.S).group(1)

SHORT_DESC = """Short"""
LONG_DESC  = """Long"""

try:
    os.stat('CHANGELOG.rst')
    LONG_DESC += "\n\n" + open('CHANGELOG.rst', 'r').read()
except OSError:
    pass

##################
### testing stuff

install_reqs = (
    'spyne>=2.12', 'lxml>=3.4.1',
)

test_reqs = install_reqs + ('pytest', 'tox')


class Tox(TestCommand):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]
    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        errno = tox.cmdline(args=shlex.split(self.tox_args))
        sys.exit(errno)

### testing stuff
##################

setup(
    name='ubl',
    packages=find_packages(),

    version=VERSION,
    description=SHORT_DESC,
    long_description=LONG_DESC,
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    keywords=('http',),
    author='Burak Arslan',
    author_email='burak+pyubl@arskom.com.tr',
    maintainer='Burak Arslan',
    maintainer_email='burak+pyubl@arskom.com.tr',
    url='http://github.com/plq/pyubl',
    license='BSD',
    zip_safe=False,
    install_requires=install_reqs,

    entry_points={
        'console_scripts': [ ],
    },

    package_data = {
        'ubl.const.schema': ['*.xsd'],
    },

    tests_require=test_reqs,
    cmdclass = {'test': Tox},
)
