# -*- coding: utf-8 -*-
#
# File: testProject.py
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

from Testing import ZopeTestCase
from Products.eXtremeManagement.config import *
from Products.eXtremeManagement.tests.eXtremeManagementTestCase import eXtremeManagementTestCase

from Products.eXtremeManagement.content.Project import Project
from Products.eXtremeManagement.content.ProjectFolder import ProjectFolder
from Products.eXtremeManagement.interfaces import IXMProject


class testProject(eXtremeManagementTestCase):
    """ test-cases for class(es) Project
    """

    def afterSetUp(self):
        """
        """
        self.setRoles(['Manager'])
        self.portal.invokeFactory('ProjectFolder', id='projects')
        self.projects = self.folder.projects
        self.projects.invokeFactory('Project', id='project')
        self.project = self.projects.project

    def test_interfaces(self):
        """ Test that Project plays nice with interfaces.
        """
        self.failUnless(IXMProject.implementedBy(Project))

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
        self.assertEqual(self.project.getMembers(), [])
        self.setRoles(['Manager'])
        self.membership = self.portal.portal_membership
        self.membership.addMember('employee1', 'secret', ['Employee'], [])
        self.membership.addMember('employee2', 'secret', [], [])
        self.project.manage_addLocalRoles('employee2',['Employee'])

        roleman = self.portal.acl_users.portal_role_manager
        self.assertEqual(len(roleman.listAssignedPrincipals('Employee')), 1)

        # Local roles are mentioned before global roles.
        # By default global and local roles are included.
        self.assertEqual(self.project.getMembers(), ['employee2', 'employee1'])

        self.project.setIncludeGlobalMembers(False)
        self.assertEqual(self.project.getMembers(), ['employee2'])

    # from class Project:
    def test_Projectteam(self):
        """
        """
        #Uncomment one of the following lines as needed
    # from class Project:
    def test_currentIteration(self):
        pass

    # Manually created methods

    def test_CurrentIteration(self):
        # Add three iterations
        self.project.invokeFactory('Iteration', id='iteration1')
        self.project.invokeFactory('Iteration', id='iteration2')
        self.project.invokeFactory('Iteration', id='iteration3')
        iteration1 = self.project.iteration1
        iteration2 = self.project.iteration2
        iteration3 = self.project.iteration3

        self.workflow = self.portal.portal_workflow
        self.assertEqual(self.project.currentIteration(), None)

        self.workflow.doActionFor(iteration1, 'start')
        self.assertEqual(self.project.currentIteration(), iteration1)
        self.workflow.doActionFor(iteration1, 'complete')
        self.assertEqual(self.project.currentIteration(), None)
        self.workflow.doActionFor(iteration1, 'invoice')
        self.assertEqual(self.project.currentIteration(), None)

        # What happens if two iterations are in-progress?
        self.workflow.doActionFor(iteration2, 'start')
        self.assertEqual(self.project.currentIteration(), iteration2)
        self.workflow.doActionFor(iteration3, 'start')
        self.assertEqual(self.project.currentIteration(), iteration2)
        self.workflow.doActionFor(iteration2, 'complete')
        self.assertEqual(self.project.currentIteration(), iteration3)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testProject))
    return suite

##code-section module-footer #fill in your manual code here
##/code-section module-footer

if __name__ == '__main__':
    framework()


