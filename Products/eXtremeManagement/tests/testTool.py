import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing import ZopeTestCase

from Products.CMFCore.utils import getToolByName

from Products.eXtremeManagement.config import *
from Products.eXtremeManagement.tests.eXtremeManagementTestCase import eXtremeManagementTestCase
from Products.eXtremeManagement.tools.eXtremeManagementTool import eXtremeManagementTool


class testTool(eXtremeManagementTestCase):
    """Test-cases for class(es) eXtremeManagementTool."""

    def afterSetUp(self):
        self.xm_tool = self.portal.xm_tool

    # from class eXtremeManagementTool:
    def test_formatTime(self):
        self.assertEqual(self.xm_tool.formatTime(0),'0:00')
        self.assertEqual(self.xm_tool.formatTime(-0.6),'-0:36')
        self.assertEqual(self.xm_tool.formatTime(0.6),'0:36')
        self.assertEqual(self.xm_tool.formatTime(-1),'-1:00')
        self.assertEqual(self.xm_tool.formatTime(1),'1:00')
        self.assertEqual(self.xm_tool.formatTime(1.5),'1:30')
        self.assertEqual(self.xm_tool.formatTime(-1.5),'-1:30')
        # .04*60 == 2.3999999999999999, which should be rounded down:
        self.assertEqual(self.xm_tool.formatTime(0.04),'0:02')
        self.assertEqual(self.xm_tool.formatTime(8.05),'8:03')
        self.assertEqual(self.xm_tool.formatTime(44.5),'44:30')
        self.assertEqual(self.xm_tool.formatTime(0.999),'1:00')

    # from class eXtremeManagementTool:
    def test_formatMinutes(self):
        self.assertEqual(self.xm_tool.formatMinutes(-1),False)
        self.assertEqual(self.xm_tool.formatMinutes(0),':00')
        self.assertEqual(self.xm_tool.formatMinutes(5),':05')
        self.assertEqual(self.xm_tool.formatMinutes(24),':24')
        self.assertEqual(self.xm_tool.formatMinutes(59),':59')
        self.assertEqual(self.xm_tool.formatMinutes(60),False)

    # from class eXtremeManagementTool:
    def test_getProjectsToList(self):
        pass

    # from class eXtremeManagementTool:
    def test_getIssues(self):
        pass


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testTool))
    return suite


if __name__ == '__main__':
    framework()
