from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent
import transaction

from Products.eXtremeManagement.tests.base import eXtremeManagementTestCase
from Products.eXtremeManagement.tests.base import reset_request
from utils import createBooking


class testStory(eXtremeManagementTestCase):
    """ test-cases for class Story
    """

    def afterSetUp(self):
        pass


    def test_EstimateAndActual(self):
        """
        When a story has tasks, get their estimates.
        If not, get the roughEstimate of this story.

        Also test ActualHours while we are at it.
        """
        # It is best to create a completely new story here.
        iteration = self.portal.project.iteration
        iteration.invokeFactory('Story', id='st')
        story = iteration.st
        story.update(roughEstimate=1.5)
        notify(ObjectModifiedEvent(story))

        self.assertEqual(story.getRoughEstimate(), 1.5)
        xm_props = self.portal.portal_properties.xm_properties
        hours_per_day = xm_props.hours_per_day
        self.assertEqual(hours_per_day, 8.0)

        # Add a Task.
        workflow = self.portal.portal_workflow
        workflow.doActionFor(story, 'estimate')
        story.invokeFactory('Task', id='task')
        task = story.task
        self.assertAnnotationStoryBrainEstimateEquality(story, 0.0)
        task.update(hours=4)
        notify(ObjectModifiedEvent(task))
        self.assertAnnotationStoryBrainEstimateEquality(story, 4.0)
        createBooking(task, id='booking1', hours=1)
        self.assertAnnotationStoryBrainHoursEquality(story, 1)

        # Add another task.
        story.invokeFactory('Task', id='2')
        task2 = story['2']
        task2.update(hours=2)
        notify(ObjectModifiedEvent(task2))
        self.assertAnnotationStoryBrainEstimateEquality(story, 6)
        createBooking(task2, id='booking1', hours=1)
        self.assertAnnotationStoryBrainHoursEquality(story, 2)

        # make a copy to test later
        copydata = iteration.manage_copyObjects(story.getId())
        iteration.manage_pasteObjects(copydata)
        copy = iteration.copy_of_st

        # make sure deleting a task updates the story's catalog entry
        story.manage_delObjects(ids=['task'])
        self.assertAnnotationStoryBrainEstimateEquality(story, 2)
        self.assertAnnotationStoryBrainHoursEquality(story, 1)

        # Make sure the copy retained it's info
        reset_request(copy)
        self.assertAnnotationStoryBrainEstimateEquality(copy, 6)
        self.assertAnnotationStoryBrainHoursEquality(copy, 2)

        # Check that cutting and pasting also works correctly with
        # respect to the estimates (and the booked hours, etc, but
        # that should be fine.
        # First make a second story for pasting into.
        iteration.invokeFactory('Story', id='story2')
        story2 = iteration.story2
        reset_request(story2)
        self.assertAnnotationStoryBrainEstimateEquality(story2, 0)
        self.assertAnnotationStoryBrainHoursEquality(story2, 0)

        # We need to commit a few times, before this works in tests.
        transaction.savepoint(optimistic=True)
        cut_data = story.manage_cutObjects(ids=['2'])
        story2.manage_pasteObjects(cut_data)
        self.assertAnnotationStoryBrainEstimateEquality(story, 0.0)
        self.assertAnnotationStoryBrainHoursEquality(story, 0)
        self.assertAnnotationStoryBrainEstimateEquality(story2, 2)
        self.assertAnnotationStoryBrainHoursEquality(story2, 1)

        # The recalc method is tested in xm.booking, but we can at
        # least call it once here.
        story.recalc()

    def test_isEstimated(self):
        """
        """
        self.loginAsPortalOwner()
        story = self.portal.project.iteration.story
        self.assertEqual(story.isEstimated(), True)
        story.update(roughEstimate=0)
        self.assertEqual(story.isEstimated(), False)
        self.logout()

    def test_startable_completed(self):
        # It is best to create a completely new story here.
        iteration = self.portal.project.iteration
        iteration.invokeFactory('Story', id='st')
        story = iteration.st

        # Stories start out as not startable and not completed.  It is
        # completable because it has no tasks that are not completed
        # yet - because it has no tasks at all; oh well.
        self.failIf(story.startable())
        self.failUnless(story.completable())
        self.failIf(story.isCompleted())

        # We give it a rough estimate but that has no effect.
        story.update(roughEstimate=1.5)
        self.failIf(story.startable())
        self.failUnless(story.completable())
        self.failIf(story.isCompleted())

        # Add a Task.
        workflow = self.portal.portal_workflow
        workflow.doActionFor(story, 'estimate')
        story.invokeFactory('Task', id='task')
        task = story.task
        self.failIf(story.startable())
        self.failIf(story.completable())
        self.failIf(story.isCompleted())

        # Make tasks startable.
        task.update(hours=4, assignees='developer')
        self.failUnless(story.startable())
        self.failIf(story.completable())
        self.failIf(story.isCompleted())

        # Activate the story
        workflow = self.portal.portal_workflow
        workflow.doActionFor(story, 'activate')
        self.failUnless(story.startable())
        self.failIf(story.completable())
        self.failIf(story.isCompleted())

        # Complete the task.  That transitions the story also automatically.
        workflow.doActionFor(task, 'complete')
        self.failUnless(story.startable())
        self.failUnless(story.completable())
        self.failUnless(story.isCompleted())

        # We reactivate the story.  It is still completable then.
        workflow.doActionFor(story, 'improve')
        self.failUnless(story.startable())
        self.failUnless(story.completable())
        self.failIf(story.isCompleted())

        # When the task get reactivated the story stays is not
        # completable anymore.
        workflow.doActionFor(task, 'reactivate')
        self.failUnless(story.startable())
        self.failIf(story.completable())
        self.failIf(story.isCompleted())


    def test_generateUniqueId(self):
        # The generateUniqueId method is called when a content type
        # gets added to this story.
        story = self.portal.project.iteration.story

        # The default is like this: 'foo_type.2008-05-20.3289113493'
        self.failUnless(
            story.generateUniqueId('Foo Type').startswith('foo_type.'))

        # When adding Tasks we choose integer ids.  We have one task
        # already, but it has no integer id, so the next unique id
        # should be 1:
        self.assertEqual(story.generateUniqueId('Task'), '1')

        # This id gets used for new tasks.  But that is hard to test
        # here with invokeFactory.  We will just pretend that it works
        # and see if the generateUniqueId function can handle what we
        # throw at it.
        story.invokeFactory('Task', '1')
        self.assertEqual(story.generateUniqueId('Task'), '2')

        # Any content items that somehow have a non integer id, should
        # not give errors.
        story.invokeFactory('Task', 'non-integer-id')
        self.assertEqual(story.generateUniqueId('Task'), '2')

        # If we add a task with a 'too high' id so it leaves a gap, we
        # do not try to be clever and fill the gaps.
        story.invokeFactory('Task', '9')
        self.assertEqual(story.generateUniqueId('Task'), '10')

        # PoiTasks should get the same treatment
        self.assertEqual(story.generateUniqueId('PoiTask'), '10')
        story.invokeFactory('PoiTask', '15')
        self.assertEqual(story.generateUniqueId('Task'), '16')
        self.assertEqual(story.generateUniqueId('PoiTask'), '16')



    def assertStoryBrainEquality(self, attribute, value, story=None):
        """Test equality of Story and storybrain from catalog.
        """
        if story is None:
            story = self.portal.project.iteration.story
        catalog = self.portal.portal_catalog
        storybrains = catalog(portal_type='Story',
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
