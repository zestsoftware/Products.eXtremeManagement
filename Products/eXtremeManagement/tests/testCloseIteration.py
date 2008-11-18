import unittest
import doctest
from zope.component import testing

OPTIONFLAGS = (doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(
        doctest.DocTestSuite('Products.eXtremeManagement.browser.closing',
                             optionflags=OPTIONFLAGS,
                             setUp=testing.setUp,
                             tearDown=testing.tearDown))
    return suite
