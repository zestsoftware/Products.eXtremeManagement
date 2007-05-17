#! /usr/bin/env python2.4

import unittest
from zope.component import testing
from zope.testing.doctestunit import DocTestSuite

base_modulestring = 'Products.eXtremeManagement.'
modules = (
    'browser.bookings',
    'browser.iterations',
    'browser.poi',
    )


class testDocUnitTests:
    """
    """
    pass


def setUp(test):
    testing.setUp(test)

def tearDown(test):
    testing.tearDown(test)

def test_suite():
    suites = unittest.TestSuite()
    for mod in modules:
        mod = base_modulestring + mod
        suite = DocTestSuite(module=mod,
                             setUp=setUp,
                             tearDown=tearDown)
        suites.addTest(suite)

    return suites
