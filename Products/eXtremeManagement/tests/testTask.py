from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent

from Products.PloneTestCase.setup import default_user

from Products.eXtremeManagement.tests.base import eXtremeManagementTestCase
from Products.eXtremeManagement.tests.base import reset_request
from Products.eXtremeManagement.tests.utils import createBooking


class testTask(eXtremeManagementTestCase):
    """ test-cases for class Task
    """

    def afterSetUp(self):
        self.story = self.portal.project.iteration.story
        self.task = self.story.task

    def test__get_assignees(self):
        self.assertEqual(self.task._get_assignees().items(),
                         ((default_user, default_user),
                          ('developer', 'developer'),
                          ('employee', 'employee')))

    def test_getRawEstimate(self):
        """Make sure rawEstimate returns the expected value.

        Also make sure the same value is stored in the catalog.
        """
        self.assertAnnotationTaskBrainEstimateEquality(self.task, 5.50)

        self.task.update(hours=0, minutes=0)
        notify(ObjectModifiedEvent(self.task))
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
        self.assertAnnotationTaskBrainHoursEquality(self.task, 3.25)

        createBooking(self.task, id='booking2', minutes=15)
        self.assertAnnotationTaskBrainHoursEquality(self.task, 3.5)

        # make a copy to test later

        copydata = self.story.manage_copyObjects(self.task.getId())
        self.story.manage_pasteObjects(copydata)
        copy = self.story.copy_of_task

        # If a Booking gets deleted, its parent task should be
        # reindexed.

        self.task.manage_delObjects('booking2')
        self.assertAnnotationTaskBrainHoursEquality(self.task, 3.25)
        self.task.manage_delObjects('booking')
        self.assertAnnotationTaskBrainHoursEquality(self.task, 0)

        # Make sure the copy retained it's info
        reset_request(copy)
        self.assertAnnotationTaskBrainHoursEquality(copy, 3.5)

        # Test cutting Bookings.
        cutdata = copy.manage_cutObjects(ids=['booking', 'booking2'])
        self.story.invokeFactory('Task', id='task3')
        task3 = self.story.task3
        task3.manage_pasteObjects(cutdata)
        self.assertAnnotationTaskBrainHoursEquality(copy, 0)
        reset_request(copy)
        self.assertAnnotationTaskBrainHoursEquality(task3, 3.5)

    def test_startable(self):
        """
        """
        self.story.invokeFactory('Task', 'task2')
        task = self.story.task2

        workflow = self.portal.portal_workflow
        self.assertEqual(workflow.getInfoFor(task, 'review_state'),
                         'open')
        self.assertEqual(task.startable(), False)
        task.update(hours=0)
        self.assertEqual(task.startable(), False)
        task.update(hours=-1)
        self.assertEqual(task.startable(), False)
        task.update(hours=1)
        self.assertEqual(task.startable(), True)
        # Having assignees or not does not matter anymore:
        task.update(assignees='developer')
        self.assertEqual(task.startable(), True)
        task.update(hours=0)
        self.assertEqual(task.startable(), False)
        task.update(minutes=-15)
        self.assertEqual(task.startable(), False)
        task.update(minutes=15)
        self.assertEqual(task.startable(), True)

        self.story.invokeFactory('Task', id='task3')
        task3 = self.story.task3
        self.assertEqual(task3.startable(), False)

        # We used to let a Task be startable without an estimate if
        # there had been a booking already, but not anymore.
        task3.invokeFactory('Booking', id='booking', minutes=15)
        self.assertEqual(task3.startable(), False)

    def test_getAssignees(self):
        #initially No assignee is selected
        self.assertTaskBrainEquality('getAssignees', ('test_user_1_',))

        self.task.update(assignees='developer')
        self.assertTaskBrainEquality('getAssignees', ('developer', ))

        self.task.update(assignees=('developer', 'employee', ))
        self.assertTaskBrainEquality('getAssignees',
                                     ('developer', 'employee', ))

        self.task.update(assignees='')
        self.assertTaskBrainEquality('getAssignees', ())


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testTask))
    return suite
