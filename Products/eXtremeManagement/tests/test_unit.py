#! /usr/bin/env python2.4

import unittest
from zope.component import testing
from zope.testing.doctestunit import DocTestSuite
from zope.testing import doctest

base_modulestring = 'Products.eXtremeManagement.'
modules = (
    'browser.bookings',
    'browser.iterations',
    'browser.poi',
    'utils',
    )


class testDocUnitTests:
    """
    """
    pass


def setUp(test):
    testing.setUp(test)

def tearDown(test):
    testing.tearDown(test)

OPTIONFLAGS = (doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)


def test_suite():
    suites = unittest.TestSuite()
    for mod in modules:
        mod = base_modulestring + mod
        suite = DocTestSuite(module=mod,
                             optionflags=OPTIONFLAGS,
                             setUp=setUp,
                             tearDown=tearDown)
        suites.addTest(suite)

    return suites
