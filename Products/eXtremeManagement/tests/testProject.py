# -*- coding: utf-8 -*-
#
# File: testProject.py
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
# Test-cases for class(es) Project
#

from Testing import ZopeTestCase
from Products.eXtremeManagement.config import *
from Products.eXtremeManagement.tests.eXtremeManagementTestCase import eXtremeManagementTestCase

# Import the tested classes
from Products.eXtremeManagement.content.Project import Project

##code-section module-beforeclass #fill in your manual code here
from Products.eXtremeManagement.content.ProjectFolder import ProjectFolder
##/code-section module-beforeclass


class testProject(eXtremeManagementTestCase):
    """ test-cases for class(es) Project
    """

    ##code-section class-header_testProject #fill in your manual code here
    ##/code-section class-header_testProject

    def afterSetUp(self):
        """
        """
        pass

    # from class Project:
    def test_getProject(self):
        """ Test that you can add and call a Project item
        """
        self.loginAsPortalOwner()
        p=ProjectFolder('projects01')
        self.portal._setObject('projects01',p)
        self.failUnless( self.portal.projects01.portal_type == 'ProjectFolder')
        
        o=Project('temp_Project')
        self.portal.projects01._setObject('temp_Project', o)
        self.failUnless( self.portal.projects01.temp_Project.portal_type == 'Project')

    # from class Project:
    def test_getMembers(self):
        """
        """
        #Uncomment one of the following lines as needed
        ##self.loginAsPortalOwner()
        ##o=Project('temp_Project')
        ##self.folder._setObject('temp_Project', o)
        pass

    # from class Project:
    def test_Projectteam(self):
        """
        """
        #Uncomment one of the following lines as needed
        ##self.loginAsPortalOwner()
        ##o=Project('temp_Project')
        ##self.folder._setObject('temp_Project', o)
        pass

    # Manually created methods


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testProject))
    return suite

##code-section module-footer #fill in your manual code here
##/code-section module-footer

if __name__ == '__main__':
    framework()


