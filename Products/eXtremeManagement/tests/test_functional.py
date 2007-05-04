"""
    eXtremeManagement functional doctests, copied from CMFPlone
    mostly.  This module collects all *.txt files in the doc directory
    and runs them.

    See also ``test_unit.py``.

"""

import os, sys

import glob
from zope.testing import doctest
import unittest
from Globals import package_home
from Testing.ZopeTestCase import FunctionalDocFileSuite as Suite
from Products.eXtremeManagement.config import GLOBALS
from Products.eXtremeManagement.tests.eXtremeManagementTestCase import eXtremeManagementFunctionalTestCase
from Products.eXtremeManagement.tests.utils import afterSetUp

REQUIRE_TESTBROWSER = [
    'time.txt',
    'create.txt',
    ]

OPTIONFLAGS = (doctest.REPORT_ONLY_FIRST_FAILURE |
               doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)

def list_doctests():
    home = package_home(GLOBALS)
    return [filename for filename in
            glob.glob(os.path.sep.join([home, 'doc', '*.txt']))]

def list_nontestbrowser_tests():
    return [filename for filename in list_doctests()
            if os.path.basename(filename) not in REQUIRE_TESTBROWSER]

def test_suite():
    # BBB: We can obviously remove this when testbrowser is Plone
    #      mainstream, read: with Five 1.4.
    try:
        import Products.Five.testbrowser
    except ImportError:
        print >> sys.stderr, ("testbrowser not found; "
                              "testbrowser tests skipped")
        filenames = list_nontestbrowser_tests()
    else:
        filenames = list_doctests()
    eXtremeManagementFunctionalTestCase.afterSetUp = afterSetUp

    suites = [Suite(os.path.basename(filename),
               optionflags=OPTIONFLAGS,
               package='Products.eXtremeManagement.doc',
               test_class=eXtremeManagementFunctionalTestCase)
              for filename in filenames]

    # BBB: Fix for http://zope.org/Collectors/Zope/2178
    from Products.PloneTestCase import layer
    from Products.PloneTestCase import setup

    if setup.USELAYER:
        for s in suites:
            if not hasattr(s, 'layer'):
                s.layer = layer.PloneSite

    return unittest.TestSuite(suites)
