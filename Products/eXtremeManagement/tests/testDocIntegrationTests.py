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


def test_suite():
    from Testing.ZopeTestCase.zopedoctest import ZopeDocFileSuite
    eXtremeManagementTestCase.afterSetUp = utils.afterSetUp

    suite = ZopeDocFileSuite('portlets.txt',
                             package='Products.eXtremeManagement.doc',
                             test_class=eXtremeManagementTestCase)
    if test_layer is not None:
        suite.layer = test_layer

    return unittest.TestSuite((suite,))

if __name__ == '__main__':
    framework()


