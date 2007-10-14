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
from Testing.ZopeTestCase import FunctionalDocFileSuite as Suite
from Products.eXtremeManagement.config import GLOBALS
from Products.eXtremeManagement.tests.eXtremeManagementTestCase import eXtremeManagementFunctionalTestCase
from Products.eXtremeManagement.tests.utils import afterSetUp

OPTIONFLAGS = (doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)


def list_doctests():
    home = package_home(GLOBALS)
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

    # BBB: Fix for http://zope.org/Collectors/Zope/2178
    from Products.PloneTestCase import layer
    from Products.PloneTestCase import setup

    if setup.USELAYER:
        for s in suites:
            if not hasattr(s, 'layer'):
                s.layer = layer.PloneSite

    return unittest.TestSuite(suites)
