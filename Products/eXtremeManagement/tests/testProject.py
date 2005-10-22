# File: testProject.py
# 
# Copyright (c) 2005 by Zest software 2005
# Generator: ArchGenXML Version 1.4.0-beta2 devel 
#            http://plone.org/products/archgenxml
#
# GNU General Public Licence (GPL)
# 
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place, Suite 330, Boston, MA  02111-1307  USA
#
__author__  = '''Ahmad Hadi <a.hadi@zestsoftware.nl>'''
__docformat__ = 'plaintext'

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

##code-section module-header #fill in your manual code here
##/code-section module-header

#
# test-cases for class(es) Project
#
import os, sys
from Testing import ZopeTestCase
from Products.eXtremeManagement.tests.eXtremeManagementTestCase import eXtremeManagementTestCase
# import the tested classes
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
        p=ProjectFolder('projects')
        self.portal._setObject('projects',p)
        self.failUnless( self.portal.projects.portal_type == 'ProjectFolder')
        
        o=Project('temp_Project')
        self.portal.projects._setObject('temp_Project', o)
        self.failUnless( self.portal.projects.temp_Project.portal_type == 'Project')


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


