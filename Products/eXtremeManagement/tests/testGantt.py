import unittest
import doctest

OPTIONFLAGS = (doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(
        doctest.DocTestSuite('Products.eXtremeManagement.browser.gantt',
                             optionflags=OPTIONFLAGS))
    return suite
