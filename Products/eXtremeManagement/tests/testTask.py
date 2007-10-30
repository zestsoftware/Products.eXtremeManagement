from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent

from Products.CMFCore.utils import getToolByName

from Products.eXtremeManagement.tests.base import eXtremeManagementTestCase
from Products.eXtremeManagement.tests.utils import createBooking


class testTask(eXtremeManagementTestCase):
    """ test-cases for class Task
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
        self.story.update(roughEstimate=1.5)
        self.workflow.doActionFor(self.story, 'estimate')
        self.story.invokeFactory('Task', id='task')
        self.task = self.story.task

    def test__get_assignees(self):
        self.assertEqual(self.task._get_assignees().items(),
                         (('developer', 'developer'),
                          ('employee', 'employee')))
        self.project.manage_addLocalRoles('klant',['Employee'])
        self.assertEqual(self.task._get_assignees().items(),
                         (('klant', 'klant'),
                          ('developer', 'developer'),
                          ('employee', 'employee')))

    def test_getRawEstimate(self):
        """Make sure rawEstimate returns the expected value.

        Also make sure the same value is stored in the catalog.
        """
        self.assertAnnotationTaskBrainEstimateEquality(self.task, 0)

        self.task.update(hours=4)
        notify(ObjectModifiedEvent(self.task))

        self.assertAnnotationTaskBrainEstimateEquality(self.task, 4)

        self.task.update(minutes=15)
        notify(ObjectModifiedEvent(self.task))
        self.assertAnnotationTaskBrainEstimateEquality(self.task, 4.25)

    def test_ActualHours(self):
        """Make sure rawActualHours returns the expected value.

        Also make sure the same value is stored in the catalog.
        """
        self.assertAnnotationTaskBrainHoursEquality(self.task, 0)

        createBooking(self.task, id='booking', hours=1)
        self.assertAnnotationTaskBrainHoursEquality(self.task, 1)

        createBooking(self.task, id='booking2', minutes=15)
        self.assertAnnotationTaskBrainHoursEquality(self.task, 1.25)

        # make a copy to test later
        
        copydata = self.story.manage_copyObjects(self.task.getId())
        self.story.manage_pasteObjects(copydata)
        copy = self.story.copy_of_task

        # If a Booking gets deleted, its parent task should be
        # reindexed.

        self.task.manage_delObjects('booking2')
        self.assertAnnotationTaskBrainHoursEquality(self.task, 1)
        self.task.manage_delObjects('booking')
        self.assertAnnotationTaskBrainHoursEquality(self.task, 0)

        # Make sure the copy retained it's info
        self.assertAnnotationTaskBrainHoursEquality(copy, 1.25)

        # Test cutting Bookings.
        cutdata = copy.manage_cutObjects(ids=['booking', 'booking2'])
        self.story.invokeFactory('Task', id='task3')
        task3 = self.story.task3
        task3.manage_pasteObjects(cutdata)
        self.assertAnnotationTaskBrainHoursEquality(copy, 0)
        self.assertAnnotationTaskBrainHoursEquality(task3, 1.25)

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
        self.task.update(assignees=('',))
        self.assertEqual(self.task.startable(), False)

        self.story.invokeFactory('Task', id='task2')
        self.task2 = self.story.task2
        self.task2.update(assignees='developer')
        self.assertEqual(self.task2.startable(), False)

        # We used to let a Task be startable without an estimate if
        # there had been a booking already, but not anymore.
        self.task2.invokeFactory('Booking', id='booking', minutes=15)
        self.assertEqual(self.task2.startable(), False)

    def test_getAssignees(self):
        self.assertTaskBrainEquality('getAssignees', ())

        self.task.update(assignees='developer')
        self.assertTaskBrainEquality('getAssignees', ('developer',))

        self.task.update(assignees=('developer','employee',))
        self.assertTaskBrainEquality('getAssignees', ('developer','employee',))

        self.task.update(assignees='')
        self.assertTaskBrainEquality('getAssignees', ())

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
