# -*- coding: utf-8 -*-
#
# File: testSetup.py
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

from Products.CMFCore.utils import getToolByName

##/code-section module-header

#
# Setup tests
#

import os, sys
from Testing import ZopeTestCase
from Products.eXtremeManagement.tests.eXtremeManagementTestCase import eXtremeManagementTestCase

class testSetup(eXtremeManagementTestCase):
    """ Test cases for the generic setup of the product
    """

    ##code-section class-header_testSetup #fill in your manual code here
    ##/code-section class-header_testSetup

    def afterSetUp(self):
        """
        """
        pass

    def test_tools(self):
        """
        """
        ids = self.portal.objectIds()
        self.failUnless('archetype_tool' in ids)

    def test_types(self):
        """
        """
        ids = self.portal.portal_types.objectIds()
        self.failUnless('CustomerFolder' in ids)
        self.failUnless('Customer' in ids)
        self.failUnless('ProjectMember' in ids)
        self.failUnless('ProjectFolder' in ids)
        self.failUnless('Project' in ids)
        self.failUnless('Iteration' in ids)
        self.failUnless('Story' in ids)
        self.failUnless('Task' in ids)
        self.failUnless('Booking' in ids)

    def test_skins(self):
        """
        """
        ids = self.portal.portal_skins.objectIds()
        self.failUnless('eXtremeManagement' in ids)

    def test_workflows(self):
        ids = self.portal.portal_workflow.objectIds()
        self.failUnless('eXtreme_Project_Workflow' in ids)
        self.failUnless('eXtreme_Iteration_Workflow' in ids)
        self.failUnless('eXtreme_Story_Workflow' in ids)
        self.failUnless('eXtreme_Task_Workflow' in ids)
        self.failUnless('eXtreme_Default_Workflow' in ids)
        self.failUnless('folder_workflow' in ids)

    def test_workflowChains(self):
        getChain = self.portal.portal_workflow.getChainForPortalType

        self.failUnless('eXtreme_Project_Workflow' in getChain('Project'))
        self.failUnless('eXtreme_Iteration_Workflow' in getChain('Iteration'))
        self.failUnless('eXtreme_Story_Workflow' in getChain('Story'))
        self.failUnless('eXtreme_Task_Workflow' in getChain('Task'))
        self.failUnless('folder_workflow' in getChain('CustomerFolder'))
        self.failUnless('folder_workflow' in getChain('ProjectFolder'))
        self.failUnless('eXtreme_Default_Workflow' in getChain('Customer'))
        self.failUnless('eXtreme_Booking_Workflow' in getChain('Booking'))
        self.failUnless('eXtreme_Default_Workflow' in getChain('ProjectMember'))

    def test_customizePortal(self):
        """
        """
        props_tool = getToolByName(self.portal, 'portal_properties')
        if props_tool.navtree_properties.hasProperty('rolesSeeUnpublishedContent'):
            rolesSeeUnpublishedContent = props_tool.navtree_properties.getProperty('rolesSeeUnpublishedContent')
            self.failUnless('Customer' in rolesSeeUnpublishedContent)

        if props_tool.navtree_properties.hasProperty('metaTypesNotToList'):
            metaTypesNotToList = props_tool.navtree_properties.getProperty(
                'metaTypesNotToList')
            for ptype in ('Booking','Task','ProjectMember'):
                self.failUnless(ptype in metaTypesNotToList)

    # Manually created methods

    def test_testCustomizePortal(self):
        """
        """
        #Uncomment one of the following lines as needed

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testSetup))
    return suite

##code-section module-footer #fill in your manual code here
##/code-section module-footer

if __name__ == '__main__':
    framework()


