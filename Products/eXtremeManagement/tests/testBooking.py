# -*- coding: utf-8 -*-
#
# File: testBooking.py
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
# Test-cases for class(es) Booking
#

from Testing import ZopeTestCase
from Products.eXtremeManagement.config import *
from Products.eXtremeManagement.tests.eXtremeManagementTestCase import eXtremeManagementTestCase

# Import the tested classes
from Products.eXtremeManagement.content.Booking import Booking

##code-section module-beforeclass #fill in your manual code here
##/code-section module-beforeclass


class testBooking(eXtremeManagementTestCase):
    """ test-cases for class(es) Booking
    """

    ##code-section class-header_testBooking #fill in your manual code here
    ##/code-section class-header_testBooking

    def afterSetUp(self):
        self.catalog = self.portal.portal_catalog
        self.workflow = self.portal.portal_workflow
        self.membership = self.portal.portal_membership

        self.setRoles(['Manager'])
        self.membership.addMember('employee', 'secret', ['Employee'], [])
        self.membership.addMember('developer', 'secret', ['Employee'], [])
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
        self.task.invokeFactory('Booking', id='booking', hours=3, minutes=15)
        self.booking = self.task.booking

    # from class Booking:
    def test__renameAfterCreation(self):
        """
        """
        #Uncomment one of the following lines as needed
    # from class Booking:
    def test_getRawActualHours(self):
        """
        """
        #Uncomment one of the following lines as needed
        ##self.loginAsPortalOwner()
        ##o=Booking('temp_Booking')
        ##self.folder._setObject('temp_Booking', o)
        self.assertEqual(self.booking.getRawActualHours(), 3.25)

        self.task.invokeFactory('Booking', id='booking2', hours=0, minutes=0)
        self.assertEqual(self.task.booking2.getRawActualHours(), 0.0)

        self.task.invokeFactory('Booking', id='booking3', hours=0, minutes=45)
        self.assertEqual(self.task.booking3.getRawActualHours(), 0.75)

        # The following two have a weird number of minutes, but if
        # they pass, that is fine.
        self.task.invokeFactory('Booking', id='booking4', hours=4, minutes=60)
        self.assertEqual(self.task.booking4.getRawActualHours(), 5.0)

        self.task.invokeFactory('Booking', id='booking5', hours=4, minutes=75)
        self.assertEqual(self.task.booking5.getRawActualHours(), 5.25)

        # What happens if hours or minutes are empty strings?
        self.task.invokeFactory('Booking', id='booking6', hours='', minutes=30)
        self.assertEqual(self.task.booking6.getRawActualHours(), 0.5)
        self.task.invokeFactory('Booking', id='booking7', hours=1, minutes='')
        self.assertEqual(self.task.booking7.getRawActualHours(), 1)

    # from class Booking:
    def test_getActualHours(self):
        """
        """
        #Uncomment one of the following lines as needed
        ##self.loginAsPortalOwner()
        ##o=Booking('temp_Booking')
        ##self.folder._setObject('temp_Booking', o)
        self.assertEqual(self.booking.getActualHours(), '3:15')

        # What happens if hours or minutes are empty strings?
        self.task.invokeFactory('Booking', id='booking1', hours='', minutes=30)
        self.assertEqual(self.task.booking1.getActualHours(), '0:30')
        self.task.invokeFactory('Booking', id='booking2', hours=1, minutes='')
        self.assertEqual(self.task.booking2.getActualHours(), '1:00')

    # Manually created methods


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testBooking))
    return suite

##code-section module-footer #fill in your manual code here
##/code-section module-footer

if __name__ == '__main__':
    framework()


