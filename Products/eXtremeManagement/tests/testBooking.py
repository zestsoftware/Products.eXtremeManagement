import os, sys

from Testing import ZopeTestCase

from Products.eXtremeManagement.config import *
from Products.eXtremeManagement.tests.eXtremeManagementTestCase import eXtremeManagementTestCase
from Products.eXtremeManagement.content.Booking import Booking
from Products.eXtremeManagement.interfaces import IXMBooking


class testBooking(eXtremeManagementTestCase):
    """ test-cases for class(es) Booking
    """

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
        self.story.update(roughEstimate=1.5)
        self.workflow.doActionFor(self.story, 'estimate')
        self.story.invokeFactory('Task', id='task')
        self.task = self.story.task
        self.task.invokeFactory('Booking', id='booking', hours=3, minutes=15)
        self.booking = self.task.booking

    def test_interfaces(self):
        """ Test that Booking plays nice with interfaces.
        """
        self.failUnless(IXMBooking.implementedBy(Booking))
        self.failUnless(IXMBooking.providedBy(self.booking))

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


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testBooking))
    return suite
