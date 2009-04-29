import os
import glob
import unittest
from Globals import package_home
from Products.eXtremeManagement.config import xm_globals
from zope.testing.doctestunit import DocTestSuite
from zope.testing import doctest, doctestunit

base_modulestring = 'Products.eXtremeManagement.'
modules = (
    'browser.bookings',
    'browser.iterations',
    'browser.poi',
    'browser.tasks',
    'browser.releaseplan',
    'emails',
    'utils',
    )

OPTIONFLAGS = (doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)


def list_doctests():
    home = package_home(xm_globals)
    return [filename for filename in
            glob.glob(os.path.sep.join([home, 'doc', 'unit_*.txt']))]


def test_suite():
    suites = unittest.TestSuite()
    # run the unit tests in the modules
    for mod in modules:
        mod = base_modulestring + mod
        suite = DocTestSuite(module=mod,
                             optionflags=OPTIONFLAGS)
        suites.addTest(suite)
    # run the unit tests which are doctests
    for doc in list_doctests():
        suites.addTest(
        doctestunit.DocFileSuite(
            os.path.basename(doc),
            package='Products.eXtremeManagement.doc',
            optionflags=OPTIONFLAGS))

    return suites
