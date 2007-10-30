from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent
import transaction

from Products.eXtremeManagement.tests.base import eXtremeManagementTestCase
from utils import createBooking


class testStory(eXtremeManagementTestCase):
    """ test-cases for class Story
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
        self.story.update(roughEstimate=4.5)
        self.workflow.doActionFor(self.story, 'estimate')
        self.story.invokeFactory('Task', id='task')
        self.task = self.story.task

        self.catalog = self.portal.portal_catalog

    def test_EstimateAndActual(self):
        """
        When a story has tasks, get their estimates.
        If not, get the roughEstimate of this story.

        Also test ActualHours while we are at it.
        """
        self.assertEqual(self.story.getRoughEstimate(), 4.5)
        xm_props = self.portal.portal_properties.xm_properties
        hours_per_day = xm_props.hours_per_day
        self.assertEqual(hours_per_day, 8.0)
        self.assertAnnotationStoryBrainEstimateEquality(self.story, 0)
        self.task.update(hours=4)
        notify(ObjectModifiedEvent(self.task))

        self.assertAnnotationStoryBrainEstimateEquality(self.story, 4.0)
        createBooking(self.task, id='booking1', hours=1)
        self.assertAnnotationStoryBrainHoursEquality(self.story, 1)

        # Add a task.
        self.story.invokeFactory('Task', id='task2')
        self.task2 = self.story.task2
        self.task2.update(hours=2)
        notify(ObjectModifiedEvent(self.task2))
        self.assertAnnotationStoryBrainEstimateEquality(self.story, 6)
        createBooking(self.task2, id='booking1', hours=1)
        self.assertAnnotationStoryBrainHoursEquality(self.story, 2)

        # make a copy to test later
        
        copydata = self.iteration.manage_copyObjects(self.story.getId())
        self.iteration.manage_pasteObjects(copydata)
        copy = self.story.copy_of_story

        # make sure deleting a task updates the story's catalog entry
        self.story.manage_delObjects(ids=['task'])
        self.assertAnnotationStoryBrainEstimateEquality(self.story, 2)
        self.assertAnnotationStoryBrainHoursEquality(self.story, 1)

        # Make sure the copy retained it's info
        self.assertAnnotationStoryBrainEstimateEquality(copy, 6)
        self.assertAnnotationStoryBrainHoursEquality(copy, 2)

        # Check that cutting and pasting also works correctly with
        # respect to the estimates (and the booked hours, etc, but
        # that should be fine.
        # First make a second story for pasting into.
        self.iteration.invokeFactory('Story', id='story2')
        story2 = self.iteration.story2
        self.assertAnnotationStoryBrainEstimateEquality(story2, 0)
        self.assertAnnotationStoryBrainHoursEquality(story2, 0)

        # We need to commit a few times, before this works in tests.
        transaction.savepoint(optimistic=True)
        cut_data = self.story.manage_cutObjects(ids=['task2'])
        story2.manage_pasteObjects(cut_data)
        self.assertAnnotationStoryBrainEstimateEquality(self.story, 0.0)
        self.assertAnnotationStoryBrainHoursEquality(self.story, 0)
        self.assertAnnotationStoryBrainEstimateEquality(story2, 2)
        self.assertAnnotationStoryBrainHoursEquality(story2, 1)

    def test_isEstimated(self):
        """
        """
        self.setRoles(['Manager'])
        self.assertEqual(self.story.isEstimated(), True)
        self.story.update(roughEstimate=0)
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
