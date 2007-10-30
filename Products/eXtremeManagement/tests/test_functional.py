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
from Products.eXtremeManagement.tests.base import eXtremeManagementFunctionalTestCase
from Products.eXtremeManagement.tests.utils import afterSetUp

OPTIONFLAGS = (doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)


def list_doctests():
    home = package_home(xm_globals)
    return [filename for filename in
            glob.glob(os.path.sep.join([home, 'doc', '*.txt']))]


def test_suite():
    filenames = list_doctests()
    eXtremeManagementFunctionalTestCase.afterSetUp = afterSetUp
    suites = [Suite(os.path.basename(filename),
               optionflags=OPTIONFLAGS,
               package='Products.eXtremeManagement.doc',
               test_class=eXtremeManagementFunctionalTestCase)
              for filename in filenames]
    return unittest.TestSuite(suites)
