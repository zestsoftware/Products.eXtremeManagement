# -*- coding: utf-8 -*-
#
# File: testTask.py
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
# Test-cases for class(es) Task
#

from Testing import ZopeTestCase
from Products.eXtremeManagement.config import *
from Products.eXtremeManagement.tests.eXtremeManagementTestCase import eXtremeManagementTestCase

# Import the tested classes
from Products.eXtremeManagement.content.Task import Task

##code-section module-beforeclass #fill in your manual code here
##/code-section module-beforeclass


class testTask(eXtremeManagementTestCase):
    """ test-cases for class(es) Task
    """

    ##code-section class-header_testTask #fill in your manual code here
    ##/code-section class-header_testTask

    def afterSetUp(self):
        self.catalog = self.portal.portal_catalog
        self.workflow = self.portal.portal_workflow
        self.userfolder = self.portal.acl_users
        self.setRoles(['Manager'])
        self.userfolder._doAddUser('employee', 'secret', ['Employee'], [])
        self.userfolder._doAddUser('developer', 'secret', ['Employee'], [])
        self.portal.invokeFactory('ProjectFolder', id='projects')
        self.projects = self.folder.projects
        self.projects.invokeFactory('Project', id='project')
        self.project = self.projects.project
        self.project.invokeFactory('Iteration', id='iteration')
        self.iteration = self.project.iteration
        self.iteration.invokeFactory('Story', id='story')
        self.story = self.iteration.story
        self.story.setRoughEstimate(1.5)
        self.workflow.doActionFor(self.story, 'estimate')
        self.story.invokeFactory('Task', id='task')
        self.task = self.story.task

    # from class Task:
    def test__get_assignees(self):
        """
        """
        #Uncomment one of the following lines as needed
        ##self.loginAsPortalOwner()
        ##o=Task('temp_Task')
        ##self.folder._setObject('temp_Task', o)
        
        self.assertEqual(self.task.getAssignees(), ())
        self.task.setAssignees('developer')
        self.assertEqual(self.task.getAssignees(), ('developer',))
        self.task.setAssignees(('developer','employee',))
        self.assertEqual(self.task.getAssignees(), ('developer','employee',))
        self.task.setAssignees('')
        self.assertEqual(self.task.getAssignees(), ())

    # from class Task:
    def test_setAssignees(self):
        pass

    # from class Task:
    def test_getRawEstimate(self):
        """
        """
        #Uncomment one of the following lines as needed
        ##self.loginAsPortalOwner()
        ##o=Task('temp_Task')
        ##self.folder._setObject('temp_Task', o)
        pass

    # from class Task:
    def test_getEstimate(self):
        """
        """
        #Uncomment one of the following lines as needed
        ##self.loginAsPortalOwner()
        ##o=Task('temp_Task')
        ##self.folder._setObject('temp_Task', o)
        pass

    # from class Task:
    def test_getRawActualHours(self):
        """
        """
        #Uncomment one of the following lines as needed
        ##self.loginAsPortalOwner()
        ##o=Task('temp_Task')
        ##self.folder._setObject('temp_Task', o)
        pass

    # from class Task:
    def test_getActualHours(self):
        """
        """
        #Uncomment one of the following lines as needed
        ##self.loginAsPortalOwner()
        ##o=Task('temp_Task')
        ##self.folder._setObject('temp_Task', o)
        pass

    # from class Task:
    def test_getRawDifference(self):
        """
        """
        #Uncomment one of the following lines as needed
        ##self.loginAsPortalOwner()
        ##o=Task('temp_Task')
        ##self.folder._setObject('temp_Task', o)
        pass

    # from class Task:
    def test_getDifference(self):
        """
        """
        #Uncomment one of the following lines as needed
        ##self.loginAsPortalOwner()
        ##o=Task('temp_Task')
        ##self.folder._setObject('temp_Task', o)
        pass

    # from class Task:
    def test_CookedBody(self):
        """
        """
        #Uncomment one of the following lines as needed
        ##self.loginAsPortalOwner()
        ##o=Task('temp_Task')
        ##self.folder._setObject('temp_Task', o)
        pass

    # from class Task:
    def test_startable(self):
        """
        """
        #Uncomment one of the following lines as needed
        ##self.loginAsPortalOwner()
        ##o=Task('temp_Task')
        ##self.folder._setObject('temp_Task', o)
        self.assertEqual(self.workflow.getInfoFor(self.task,'review_state'),
                         'open')
        self.assertEqual(self.task.startable(), False)
        self.task.setAssignees('developer')
        self.assertEqual(self.task.startable(), False)
        self.task.setHours(0)
        self.assertEqual(self.task.startable(), False)
        self.task.setHours(-1)
        self.assertEqual(self.task.startable(), False)
        self.task.setHours(1)
        self.assertEqual(self.task.startable(), True)
        self.task.setHours(0)
        self.assertEqual(self.task.startable(), False)
        self.task.setMinutes(-15)
        self.assertEqual(self.task.startable(), False)
        self.task.setMinutes(15)
        self.assertEqual(self.task.startable(), True)
        self.task.setAssignees('')
        self.assertEqual(self.task.startable(), False)

    # Manually created methods


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testTask))
    return suite

##code-section module-footer #fill in your manual code here
##/code-section module-footer

if __name__ == '__main__':
    framework()


