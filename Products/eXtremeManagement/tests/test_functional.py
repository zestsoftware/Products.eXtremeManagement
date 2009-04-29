"""
    eXtremeManagement functional doctests, copied from CMFPlone
    mostly.  This module collects all *.txt files in the doc directory
    and runs them.

    See also ``test_unit.py``.

"""

import os
import glob
from zope.testing import doctest
import unittest
from Globals import package_home
from Products.eXtremeManagement.config import xm_globals
from Testing.ZopeTestCase import FunctionalDocFileSuite as Suite
from Products.eXtremeManagement.tests.base import \
    eXtremeManagementFunctionalTestCase

OPTIONFLAGS = (doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)


def list_doctests():
    home = package_home(xm_globals)
    return [filename for filename in
            glob.glob(os.path.sep.join([home, 'doc', 'func_*.txt']))]


def setUp(test):
    # A test request needs to be annotatable as we use memoize.
    from zope.publisher.browser import TestRequest
    from zope.annotation.interfaces import IAttributeAnnotatable
    from zope.interface import classImplements
    classImplements(TestRequest, IAttributeAnnotatable)


def test_suite():
    filenames = list_doctests()
    suites = [Suite(os.path.basename(filename),
               optionflags=OPTIONFLAGS,
               package='Products.eXtremeManagement.doc',
               setUp=setUp,
               test_class=eXtremeManagementFunctionalTestCase)
              for filename in filenames]
    return unittest.TestSuite(suites)
