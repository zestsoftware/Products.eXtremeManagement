# -*- coding: utf-8 -*-
#
# File: testProjectFolder.py
#
# Copyright (c) 2006 by Zest software
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
<m.van.rees@zestsoftware.nl>"""
__docformat__ = 'plaintext'

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

##code-section module-header #fill in your manual code here
##/code-section module-header

#
# Test-cases for class(es) ProjectFolder
#

from Testing import ZopeTestCase
from Products.eXtremeManagement.config import *
from Products.eXtremeManagement.tests.eXtremeManagementTestCase import eXtremeManagementTestCase

# Import the tested classes
from Products.eXtremeManagement.content.ProjectFolder import ProjectFolder

##code-section module-beforeclass #fill in your manual code here
##/code-section module-beforeclass


class testProjectFolder(eXtremeManagementTestCase):
    """ test-cases for class(es) ProjectFolder
    """

    ##code-section class-header_testProjectFolder #fill in your manual code here
    ##/code-section class-header_testProjectFolder

    def afterSetUp(self):
        """
        """
        self.setRoles(['Manager'])
        self.portal.invokeFactory('ProjectFolder', id='projects')
        self.projects = self.folder.projects

        self.projects.invokeFactory('Project', id='project')
        self.project = self.projects.project

    # from class ProjectFolder:
    def test_formatTime(self):
        """
        """
        self.assertEqual(self.project.formatTime(0),'0:00')
        self.assertEqual(self.project.formatTime(-0.6),'-0:36')
        self.assertEqual(self.project.formatTime(0.6),'0:36')
        self.assertEqual(self.project.formatTime(-1),'-1:00')
        self.assertEqual(self.project.formatTime(1),'1:00')
        self.assertEqual(self.project.formatTime(1.5),'1:30')
        self.assertEqual(self.project.formatTime(-1.5),'-1:30')
        # .04*60 == 2.3999999999999999, which should be rounded down:
        self.assertEqual(self.project.formatTime(0.04),'0:02')
        self.assertEqual(self.project.formatTime(8.05),'8:03')
        self.assertEqual(self.project.formatTime(44.5),'44:30')
        self.assertEqual(self.project.formatTime(0.999),'1:00')

    # from class ProjectFolder:
    def test_formatMinutes(self):
        """
        """
        self.assertEqual(self.project.formatMinutes(-1),False)
        self.assertEqual(self.project.formatMinutes(0),':00')
        self.assertEqual(self.project.formatMinutes(5),':05')
        self.assertEqual(self.project.formatMinutes(24),':24')
        self.assertEqual(self.project.formatMinutes(59),':59')
        self.assertEqual(self.project.formatMinutes(60),False)

    # from class ProjectFolder:
    def test_project_listing(self):
        pass

    # Manually created methods

    def test_projectFolder(self):
        """Test adding a ProjectFolder in the portal root
        """
        self.loginAsPortalOwner()
        p=ProjectFolder('projects01')
        self.portal._setObject('projects01',p)
        self.failUnless( self.portal.projects01.portal_type == 'ProjectFolder')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testProjectFolder))
    return suite

##code-section module-footer #fill in your manual code here
##/code-section module-footer

if __name__ == '__main__':
    framework()


