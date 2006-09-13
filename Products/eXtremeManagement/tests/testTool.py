# -*- coding: utf-8 -*-
#
# File: testTool.py
#
# Copyright (c) 2006 by Zest software, Lovely Systems
# Generator: ArchGenXML 
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

__author__ = """Ahmad Hadi <a.hadi@zestsoftware.nl>, Maurits van Rees
<m.van.rees@zestsoftware.nl>, Jodok Batlogg <jodok.batlogg@lovelysystems.com>"""
__docformat__ = 'plaintext'

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

##code-section module-header #fill in your manual code here
##/code-section module-header

#
# Test-cases for class(es) eXtremeManagementTool
#

from Testing import ZopeTestCase
from Products.eXtremeManagement.config import *
from Products.eXtremeManagement.tests.eXtremeManagementTestCase import eXtremeManagementTestCase

# Import the tested classes
from Products.eXtremeManagement.tools.eXtremeManagementTool import eXtremeManagementTool

##code-section module-beforeclass #fill in your manual code here
from Products.CMFCore.utils import getToolByName
##/code-section module-beforeclass


class testTool(eXtremeManagementTestCase):
    """Test-cases for class(es) eXtremeManagementTool."""

    ##code-section class-header_testTool #fill in your manual code here
    ##/code-section class-header_testTool

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

    # Manually created methods


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testTool))
    return suite

##code-section module-footer #fill in your manual code here
##/code-section module-footer

if __name__ == '__main__':
    framework()


