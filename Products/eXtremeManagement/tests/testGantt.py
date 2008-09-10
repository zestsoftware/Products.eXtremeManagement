import unittest
import doctest


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(
        doctest.DocTestSuite('Products.eXtremeManagement.browser.gantt'))
    return suite
