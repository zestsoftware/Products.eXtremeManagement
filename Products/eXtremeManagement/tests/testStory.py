# -*- coding: utf-8 -*-
#
# File: testStory.py
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
import transaction
from Products.eXtremeManagement.config import *
from Products.eXtremeManagement.tests.eXtremeManagementTestCase import eXtremeManagementTestCase

# Import the tested classes
from Products.eXtremeManagement.content.Story import Story
from Products.eXtremeManagement.interfaces import IXMStory


class testStory(eXtremeManagementTestCase):
    """ test-cases for class(es) Story
    """

    def afterSetUp(self):
        self.workflow = self.portal.portal_workflow
        self.membership = self.portal.portal_membership

        self.membership.addMember('customer', 'secret', ['Customer'], [])
        self.membership.addMember('employee', 'secret', ['Employee'], [])
        self.setRoles(['Manager'])
        self.portal.invokeFactory('ProjectFolder', id='projects')
        self.projects = self.folder.projects
        self.projects.invokeFactory('Project', id='project')
        self.project = self.projects.project
        self.project.manage_addLocalRoles('customer',['Customer'])
        self.project.invokeFactory('Iteration', id='iteration')
        self.iteration = self.project.iteration
        self.iteration.invokeFactory('Story', id='story')
        self.story = self.iteration.story
        self.assertEqual(self.story.isEstimated(), False)
        self.story.setRoughEstimate(4.5)
        self.workflow.doActionFor(self.story, 'estimate')
        self.story.invokeFactory('Task', id='task')
        self.task = self.story.task

        self.catalog = self.portal.portal_catalog

    def test_interfaces(self):
        """ Test that Story plays nice with interfaces.
        """
        self.failUnless(IXMStory.implementedBy(Story))

    def test_get_progress_perc(self):
        """
        """
        self.assertEqual(MAXIMUM_NOT_COMPLETED_PERCENTAGE, 90)
        self.task.update(hours=1)
        self.assertEqual(self.story.get_progress_perc(), 0)
        self.task.invokeFactory('Booking', id='booking1', hours=0, minutes=15)
        self.assertEqual(self.story.getRawActualHours(), 0.25)
        self.assertEqual(self.story.get_progress_perc(), 25)
        self.task.invokeFactory('Booking', id='booking2', hours=0, minutes=45)
        self.assertEqual(self.story.getRawActualHours(), 1.0)
        self.assertEqual(self.story.get_progress_perc(), 90)
        self.login('employee')
        self.task.setAssignees('employee')
        self.workflow.doActionFor(self.story, 'activate')
        self.workflow.doActionFor(self.task, 'complete')
        self.assertEqual(self.story.get_progress_perc(), 100)

    def test_getRawEstimateAndActual(self):
        """
        When a story has tasks, get their estimates.
        If not, get the roughEstimate of this story.
        HOURS_PER_DAY is set in AppConfig.py (probably 8).

        Also test getRawActualHours while we are at it.
        """
        self.assertEqual(self.story.getRoughEstimate(), 4.5)
        self.assertEqual(HOURS_PER_DAY, 8)
        self.assertEqual(self.story.getRawEstimate(), 4.5 * HOURS_PER_DAY)
        self.task.update(hours=4)
        self.assertEqual(self.story.getRawEstimate(), 4)
        self.assertStoryBrainEquality('getRawEstimate', 4.0)
        self.task.invokeFactory('Booking', id='booking1', hours=1)
        self.assertStoryBrainEquality('getRawActualHours', 1)

        # Add a task.
        self.story.invokeFactory('Task', id='task2')
        self.task2 = self.story.task2
        self.task2.update(hours=2)
        self.assertEqual(self.story.getRawEstimate(), 6)
        self.task2.invokeFactory('Booking', id='booking1', hours=1)
        self.assertStoryBrainEquality('getRawActualHours', 2)

        # make a copy to test later
        
        copydata = self.iteration.manage_copyObjects(self.story.getId())
        self.iteration.manage_pasteObjects(copydata)
        copy = self.story.copy_of_story

        # make sure deleting a task updates the story's catalog entry
        self.story.manage_delObjects(ids=['task'])
        self.assertStoryBrainEquality('getRawEstimate', 2)
        self.assertStoryBrainEquality('getRawActualHours', 1)

        # Make sure the copy retained it's info
        self.assertStoryBrainEquality('getRawEstimate', 6, story=copy)
        self.assertStoryBrainEquality('getRawActualHours', 2, story=copy)

        # Check that cutting and pasting also works correctly with
        # respect to the estimates (and the booked hours, etc, but
        # that should be fine.
        # First make a second story for pasting into.
        self.iteration.invokeFactory('Story', id='story2')
        story2 = self.iteration.story2
        self.assertStoryBrainEquality('getRawEstimate', 0, story=story2)
        self.assertStoryBrainEquality('getRawActualHours', 0, story=story2)

        # We need to commit a few times, before this works in tests.
        transaction.savepoint(optimistic=True)
        cut_data = self.story.manage_cutObjects(ids=['task2'])
        story2.manage_pasteObjects(cut_data)
        self.assertStoryBrainEquality('getRawEstimate', 4.5 * HOURS_PER_DAY)
        self.assertStoryBrainEquality('getRawActualHours', 0)
        self.assertStoryBrainEquality('getRawEstimate', 2, story2)
        self.assertStoryBrainEquality('getRawActualHours', 1, story=story2)

    def test_isEstimated(self):
        """
        """
        self.setRoles(['Manager'])
        self.assertEqual(self.story.isEstimated(), True)
        self.story.setRoughEstimate(0)
        self.assertEqual(self.story.isEstimated(), False)
        self.logout()

    def assertStoryBrainEquality(self, attribute, value, story=None):
        """Test equality of Story and storybrain from catalog.
        """
        if story is None:
            story = self.story
        storybrains = self.catalog(portal_type='Story',
                                  path='/'.join(story.getPhysicalPath()))

        storybrain = storybrains[0]
        self.assertEqual(story[attribute](), value)
        self.assertEqual(story[attribute](),
                         storybrain[attribute])


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testStory))
    return suite

if __name__ == '__main__':
    framework()


