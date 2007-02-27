# -*- coding: utf-8 -*-
import os
import sys
import unittest
from Testing import ZopeTestCase
from Products.eXtremeManagement.tests.eXtremeManagementTestCase import eXtremeManagementTestCase
from Products.eXtremeManagement.tests import utils

try:
    from Products.PloneTestCase.layer import PloneSite as test_layer
except:
    test_layer = None

if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

# Add any files from the doc/ directory you wish to test here.
docfiles = (
    'portlets.txt',
    )


def test_suite():
    from Testing.ZopeTestCase.zopedoctest import ZopeDocFileSuite
    eXtremeManagementTestCase.afterSetUp = utils.afterSetUp
    suites = unittest.TestSuite()
    for docfile in docfiles:
        suite = ZopeDocFileSuite(docfile,
                                 package='Products.eXtremeManagement.doc',
                                 test_class=eXtremeManagementTestCase)
        if test_layer is not None:
            suite.layer = test_layer
        suites.addTest(suite)

    return suites

if __name__ == '__main__':
    framework()


