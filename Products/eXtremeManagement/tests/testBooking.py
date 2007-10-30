from Products.eXtremeManagement.tests.base import eXtremeManagementTestCase
from xm.booking.timing.interfaces import IActualHours


class testBooking(eXtremeManagementTestCase):
    """ test-cases for class Booking
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

    def test_ActualHours(self):
        """
        """
        ann = IActualHours(self.booking)
        self.assertEqual(ann.actual_time, 3.25)

        self.task.invokeFactory('Booking', id='booking2', hours=0, minutes=0)
        ann = IActualHours(self.task.booking2)
        self.assertEqual(ann.actual_time, 0.0)

        self.task.invokeFactory('Booking', id='booking3', hours=0, minutes=45)
        ann = IActualHours(self.task.booking3)
        self.assertEqual(ann.actual_time, 0.75)

        # The following two have a weird number of minutes, but if
        # they pass, that is fine.
        self.task.invokeFactory('Booking', id='booking4', hours=4, minutes=60)
        ann = IActualHours(self.task.booking4)
        self.assertEqual(ann.actual_time, 5.0)

        self.task.invokeFactory('Booking', id='booking5', hours=4, minutes=75)
        ann = IActualHours(self.task.booking5)
        self.assertEqual(ann.actual_time, 5.25)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testBooking))
    return suite
