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
        self.project.manage_addLocalRoles('customer', ['Customer'])
        self.project.invokeFactory('Iteration', id='iteration')
        self.iteration = self.project.iteration
        self.iteration.invokeFactory('Story', id='story')
        self.story = self.iteration.story
        self.assertEqual(self.story.isEstimated(), False)
        self.story.update(roughEstimate=4.5)
        self.workflow.doActionFor(self.story, 'estimate')
        self.story.invokeFactory('Task', id='1')
        self.task = self.story['1']

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
        self.story.invokeFactory('Task', id='2')
        self.task2 = self.story['2']
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
        self.story.manage_delObjects(ids=['1'])
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
        cut_data = self.story.manage_cutObjects(ids=['2'])
        story2.manage_pasteObjects(cut_data)
        self.assertAnnotationStoryBrainEstimateEquality(self.story, 0.0)
        self.assertAnnotationStoryBrainHoursEquality(self.story, 0)
        self.assertAnnotationStoryBrainEstimateEquality(story2, 2)
        self.assertAnnotationStoryBrainHoursEquality(story2, 1)

        # The recalc method is tested in xm.booking, but we can at
        # least call it once here.
        self.story.recalc()

    def test_isEstimated(self):
        """
        """
        self.setRoles(['Manager'])
        self.assertEqual(self.story.isEstimated(), True)
        self.story.update(roughEstimate=0)
        self.assertEqual(self.story.isEstimated(), False)
        self.logout()

    def test_startable_completed(self):
        # Stories start out as not startable, not completable and not
        # completed.
        self.failIf(self.story.startable())
        self.failIf(self.story.completable())
        self.failIf(self.story.isCompleted())

        # The story has been estimated, but what if we change the
        # rough estimate back to zero?
        self.story.update(roughEstimate=0)
        self.failIf(self.story.startable())
        self.failIf(self.story.completable())
        self.failIf(self.story.isCompleted())
        self.story.update(roughEstimate=4.5)

        # Make task startable.
        self.task.update(hours=4, assignees='developer')
        self.failUnless(self.story.startable())
        self.failIf(self.story.completable())
        self.failIf(self.story.isCompleted())

        # Activate the story
        self.workflow.doActionFor(self.story, 'activate')
        self.failUnless(self.story.startable())
        self.failIf(self.story.completable())
        self.failIf(self.story.isCompleted())
        
        # Complete the task.  That transitions the story also automatically.
        self.workflow.doActionFor(self.task, 'complete')
        self.failUnless(self.story.startable())
        self.failUnless(self.story.completable())
        self.failUnless(self.story.isCompleted())

        # When the task get reactivated the story stays in the
        # completed state but is not completable anymore.
        self.workflow.doActionFor(self.task, 'reactivate')
        self.failUnless(self.story.startable())
        self.failIf(self.story.completable())
        self.failUnless(self.story.isCompleted())


    def test_generateUniqueId(self):
        # The generateUniqueId method is called when a content type
        # gets added to this story.
        story = self.story

        # The default is like this: 'foo_type.2008-05-20.3289113493'
        self.failUnless(
            story.generateUniqueId('Foo Type').startswith('foo_type.'))

        # When adding Tasks we choose integer ids.  We have one task
        # already, so the next unique id should be 2:
        self.assertEqual(story.generateUniqueId('Task'), '2')

        # This id gets used for new tasks.  But that is hard to test
        # here with invokeFactory.  We will just pretend that it works
        # and see if the generateUniqueId function can handle what we
        # throw at it.
        story.invokeFactory('Task', '2')
        self.assertEqual(story.generateUniqueId('Task'), '3')

        # Any content items that somehow have a non integer id, should
        # not give errors.
        story.invokeFactory('Task', 'non-integer-id')
        self.assertEqual(story.generateUniqueId('Task'), '3')

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
