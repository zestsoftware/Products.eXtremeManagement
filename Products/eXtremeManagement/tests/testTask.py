# -*- coding: utf-8 -*-
#
# File: testTask.py
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


from Products.eXtremeManagement.content.Task import Task
from Products.eXtremeManagement.interfaces import IXMTask

from Products.CMFCore.utils import getToolByName



class testTask(eXtremeManagementTestCase):
    """ test-cases for class(es) Task
    """

    def afterSetUp(self):
        self.catalog =  getToolByName(self.portal, 'portal_catalog')
        self.workflow = self.portal.portal_workflow
        self.setRoles(['Manager'])
        self.membership = self.portal.portal_membership
        self.membership.addMember('employee', 'secret', ['Employee'], [])
        self.membership.addMember('developer', 'secret', ['Employee'], [])
        self.membership.addMember('klant', 'secret', ['Customer'], [])
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

    def test_interfaces(self):
        """ Test that Task plays nice with interfaces.
        """
        self.failUnless(IXMTask.implementedBy(Task))

    # from class Task:
    def test__get_assignees(self):
        self.assertEqual(self.task._get_assignees().items(),
                         (('developer', 'developer'),
                          ('employee', 'employee')))
        self.project.manage_addLocalRoles('klant',['Employee'])
        self.assertEqual(self.task._get_assignees().items(),
                         (('klant', 'klant'),
                          ('developer', 'developer'),
                          ('employee', 'employee')))
        # And a little trick to please ArchGenXML, as it doesn't like
        # the previous line.
        assert(True)

    # from class Task:
    def test_setAssignees(self):
        pass

    # from class Task:
    def test_getRawEstimate(self):
        """Make sure rawEstimate returns the expected value.

        Also make sure the same value is stored in the catalog.
        """
        self.assertTaskBrainEquality('getRawEstimate', 0)

        self.task.update(hours=4)
        self.assertTaskBrainEquality('getRawEstimate', 4)

        self.task.update(minutes=15)
        self.assertTaskBrainEquality('getRawEstimate', 4.25)

    # from class Task:
    def test_getEstimate(self):
        """
        """
        pass
    # from class Task:
    def test_getRawActualHours(self):
        """Make sure rawActualHours returns the expected value.

        Also make sure the same value is stored in the catalog.
        """
        self.assertTaskBrainEquality('getRawActualHours', 0)

        self.task.invokeFactory('Booking', id='booking', hours=1)
        self.assertTaskBrainEquality('getRawActualHours', 1)

        self.task.invokeFactory('Booking', id='booking2', minutes=15)
        self.assertTaskBrainEquality('getRawActualHours', 1.25)

        # make a copy to test later
        
        copydata = self.story.manage_copyObjects(self.task.getId())
        self.story.manage_pasteObjects(copydata)
        copy = self.story.copy_of_task

        # If a Booking gets deleted, its parent task should be
        # reindexed.

        self.task.manage_delObjects('booking2')
        self.assertTaskBrainEquality('getRawActualHours', 1)
        self.task.manage_delObjects('booking')
        self.assertTaskBrainEquality('getRawActualHours', 0)

        # Make sure the copy retained it's info
        self.assertTaskBrainEquality('getRawActualHours', 1.25, task=copy)

        # Test cutting Bookings.
        cutdata = copy.manage_cutObjects(ids=['booking', 'booking2'])
        self.story.invokeFactory('Task', id='task3')
        task3 = self.story.task3
        task3.manage_pasteObjects(cutdata)
        self.assertTaskBrainEquality('getRawActualHours', 0, task=copy)
        self.assertTaskBrainEquality('getRawActualHours', 1.25, task=task3)


    # from class Task:
    def test_getActualHours(self):
        """
        """
        pass
    # from class Task:
    def test_getRawDifference(self):
        """Make sure rawDifference returns the expected value.

        Also make sure the same value is stored in the catalog.
        """
        self.assertTaskBrainEquality('getRawDifference', 0)

        self.task.update(hours=4)
        self.assertTaskBrainEquality('getRawDifference', -4)

        self.task.invokeFactory('Booking', id='booking', hours=1)
        self.assertTaskBrainEquality('getRawDifference', -3)

        self.task.invokeFactory('Booking', id='booking2', minutes=15)
        self.assertTaskBrainEquality('getRawDifference', -2.75)

    # from class Task:
    def test_getDifference(self):
        """
        """
        pass
    # from class Task:
    def test_CookedBody(self):
        """
        """
        pass
    # from class Task:
    def test_startable(self):
        """
        """
        self.assertEqual(self.workflow.getInfoFor(self.task,'review_state'),
                         'open')
        self.assertEqual(self.task.startable(), False)
        self.task.update(assignees='developer')
        self.assertEqual(self.task.startable(), False)
        self.task.update(hours=0)
        self.assertEqual(self.task.startable(), False)
        self.task.update(hours=-1)
        self.assertEqual(self.task.startable(), False)
        self.task.update(hours=1)
        self.assertEqual(self.task.startable(), True)
        self.task.update(hours=0)
        self.assertEqual(self.task.startable(), False)
        self.task.update(minutes=-15)
        self.assertEqual(self.task.startable(), False)
        self.task.update(minutes=15)
        self.assertEqual(self.task.startable(), True)
        self.task.setAssignees('')
        self.assertEqual(self.task.startable(), False)

        self.story.invokeFactory('Task', id='task2')
        self.task2 = self.story.task2
        self.task2.update(assignees='developer')
        self.assertEqual(self.task2.startable(), False)
        self.task2.invokeFactory('Booking', id='booking', minutes=15)
        self.assertEqual(self.task2.startable(), True)

    # Manually created methods

    def test_getAssignees(self):
        self.assertTaskBrainEquality('getAssignees', ())

        self.task.update(assignees='developer')
        self.assertTaskBrainEquality('getAssignees', ('developer',))

        self.task.update(assignees=('developer','employee',))
        self.assertTaskBrainEquality('getAssignees', ('developer','employee',))

        self.task.update(assignees='')
        self.assertTaskBrainEquality('getAssignees', ())

    def assertTaskBrainEquality(self, attribute, value, task=None):
        """Test equality of Task and taskbrain from catalog.
        """
        if task is None:
            task = self.task
        taskbrains = self.catalog(portal_type='Task',
                                  path='/'.join(task.getPhysicalPath()))

        taskbrain = taskbrains[0]
        self.assertEqual(task[attribute](), value)
        self.assertEqual(task[attribute](),
                         taskbrain[attribute])

    def test_getDefaultAssignee(self):
        """
        """
        self.assertEqual(self.task.getDefaultAssignee(), '')
        self.story.invokeFactory('Task', id='task1')
        self.assertEqual(self.story.task1.getAssignees(), ())

        self.login('employee')
        self.project.manage_addLocalRoles('employee',['Employee'])
        self.assertEqual(self.task.getDefaultAssignee(), 'employee')
        self.story.invokeFactory('Task', id='task2')
        self.assertEqual(self.story.task2.getAssignees(), ('employee',))

        self.login('klant')
        self.assertEqual(self.task.getDefaultAssignee(), '')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testTask))
    return suite

##code-section module-footer #fill in your manual code here
##/code-section module-footer

if __name__ == '__main__':
    framework()


