# File: testMySetup.py
"""\
NON-AGX OVERWRITTEN FILE

"""
# Copyright (c) 2005 by Zest software 2005
# Generator: ArchGenXML Version 1.4 devel 1 http://sf.net/projects/archetypes/
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

##code-section module-header #fill in your manual code here
##/code-section module-header

#
# Setup tests
#
import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.PloneTestCase import PloneTestCase
from Products.eXtremeManagement.tests.eXtremeManagementTestCase import eXtremeManagementTestCase

class TestSetup(eXtremeManagementTestCase):

    ##code-section class-header_testSetup #fill in your manual code here
    ##/code-section class-header_testSetup

    def testCustomizePortal(self,):
        pass

    def testTools(self):
        ids = self.portal.objectIds()
        self.failUnless('archetype_tool' in ids)
        #[]

    def testSkins(self):
        ids = self.portal.portal_skins.objectIds()
        self.failUnless('eXtremeManagement' in ids)

    def testCustomer(self):
        ids = self.portal.portal_types.objectIds()
        self.failUnless('Customer' in ids)

    def testCustomerFolder(self):
        ids = self.portal.portal_types.objectIds()
        self.failUnless('CustomerFolder' in ids)

    def testStory(self):
        ids = self.portal.portal_types.objectIds()
        self.failUnless('Story' in ids)
 
    def testProjectFolder(self):
        ids = self.portal.portal_types.objectIds()
        self.failUnless('ProjectFolder' in ids)

    def testProject(self):
        ids = self.portal.portal_types.objectIds()
        self.failUnless('Project' in ids)
  
    def testTask(self):
        ids = self.portal.portal_types.objectIds()
        self.failUnless('Task' in ids)

    def testIteration(self):
        ids = self.portal.portal_types.objectIds()
        self.failUnless('Iteration' in ids)

    def testWorkflows(self):
        ids = self.portal.portal_workflow.objectIds()
        self.failUnless('eXtreme_task_workflow' in ids)
        self.failUnless('eXtreme_story_workflow' in ids)
        self.failUnless('eXtreme_iteration_workflow' in ids)
        self.failUnless('eXtreme_folder_workflow' in ids)

    def testWorkflowChains(self):
        getChain = self.portal.portal_workflow.getChainForPortalType
        self.failUnless('eXtreme_task_workflow' in getChain('Task'))
        self.failUnless('eXtreme_story_workflow' in getChain('Story'))
        self.failUnless('eXtreme_iteration_workflow' in getChain('Iteration'))
        self.failUnless('eXtreme_folder_workflow' in getChain('Customer'))
        self.failUnless('eXtreme_folder_workflow' in getChain('CustomerFolder'))
        self.failUnless('eXtreme_folder_workflow' in getChain('Project'))
        self.failUnless('eXtreme_folder_workflow' in getChain('ProjectFolder'))
        self.failUnless('eXtreme_folder_workflow' in getChain('ProjectMember'))

    def test_callCustomerFolder(self):
        """ Test that you can add and call a CustomerFolder item
        """
        self.setRoles(['Manager'])
        self.portal.invokeFactory('CustomerFolder', id='testCustomerFolder')
        result = self.portal.testCustomerFolder.view()

    def test_callProjectFolder(self):
        """ Test that you can add and call a ProjectFolder item
        """
        self.setRoles(['Manager'])
        self.portal.invokeFactory('ProjectFolder', id='testProject')
        result = self.portal.testProject.view()

    def test_callProject(self):
        """ Test that you can add and call a Project item
        """
        self.setRoles(['Manager'])
        self.portal.invokeFactory('ProjectFolder', id='testProjectFolder')
        self.portal.testProjectFolder.invokeFactory('Project', id='testproject01')
        result = self.portal.testProjectFolder.testproject01.view()

    def test_callIteration(self):
        """ Test that you can add and call an Iteration
        """
        self.setRoles(['Manager'])
        self.portal.invokeFactory('ProjectFolder', id='testProjectFolder')
        self.portal.testProjectFolder.invokeFactory('Project', id='testproject01')
        self.portal.testProjectFolder.testproject01.invokeFactory('Iteration', id='testIteration')
        result = self.portal.testProjectFolder.testproject01.testIteration.view()

    def test_callStory(self):
        """ Test that you can add and call a Story item
        """
        self.setRoles(['Manager'])
        self.portal.invokeFactory('ProjectFolder', id='testProjectFolder')
        self.portal.testProjectFolder.invokeFactory('Project', id='testproject01')
        self.portal.testProjectFolder.testproject01.invokeFactory('Iteration', id='testIteration')
        self.portal.testProjectFolder.testproject01.testIteration.invokeFactory('Story', id='testStory')
        result = self.portal.testProjectFolder.testproject01.testIteration.testStory.view()
       

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestSetup))
    return suite

if __name__ == '__main__':
    framework()

##code-section module-footer #fill in your manual code here
##/code-section module-footer

