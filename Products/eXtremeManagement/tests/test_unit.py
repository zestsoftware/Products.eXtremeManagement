import unittest
from zope.testing.doctestunit import DocTestSuite
from zope.testing import doctest

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


def test_suite():
    suites = unittest.TestSuite()
    for mod in modules:
        mod = base_modulestring + mod
        suite = DocTestSuite(module=mod,
                             optionflags=OPTIONFLAGS)
        suites.addTest(suite)

    return suites
