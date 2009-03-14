from Products.CMFCore.WorkflowCore import WorkflowException
from Products.PloneTestCase.setup import default_user

from Products.eXtremeManagement.tests.base import eXtremeManagementTestCase


class testWorkflow(eXtremeManagementTestCase):
    """ test-cases for workflow
    """

    def afterSetUp(self):
        self.workflow = self.portal.portal_workflow

        self.project = self.portal.project
        self.offer = self.project.offer
        self.iteration = self.project.iteration
        self.story = self.iteration.story
        self.task = self.story.task
        self.booking = self.task.booking

    def test_initial_states(self):
        """Test if the initial states for the CTs are what we expect
        them to be.
        """

        self.assertEqual(
            self.workflow.getInfoFor(self.project, 'review_state'), 'private')
        self.assertEqual(
            self.workflow.getInfoFor(self.iteration, 'review_state'), 'new')
        # Story has been transtioned already.  Let's make a new one.
        self.iteration.invokeFactory('Story', id='story2')
        self.assertEqual(
            self.workflow.getInfoFor(self.iteration.story2, 'review_state'),
            'draft')
        self.assertEqual(
            self.workflow.getInfoFor(self.task, 'review_state'), 'open')
        self.assertEqual(
            self.workflow.getInfoFor(self.booking, 'review_state'), 'booking')

    def test_project_transitions(self):
        """Test transitions of the Project Content Type
        """
        # Manager (same as Owner here) can transition a project:
        # private -> active -> completed -> active -> private
        self.login('manager')
        self.tryAllowedTransition(self.project, 'project',
                                  'private', 'activate', 'active')
        self.tryAllowedTransition(self.project, 'project',
                                  'active', 'close', 'completed')
        self.tryAllowedTransition(self.project, 'project',
                                  'completed', 'reactivate', 'active')
        self.tryAllowedTransition(self.project, 'project',
                                  'active', 'deactivate', 'private')

        # Try some forbidden transactions
        self.login('reviewer')
        self.tryForbiddenTransition(self.project, 'private', 'activate')
        self.login('employee')
        self.tryForbiddenTransition(self.project, 'private', 'activate')
        self.login('customer')
        self.tryForbiddenTransition(self.project, 'private', 'activate')

        # Try some transactions that don't belong to the current state
        self.login('manager')
        self.tryForbiddenTransition(self.project, 'private', 'reactivate')
        self.tryAllowedTransition(self.project, 'project',
                                  'private', 'activate', 'active')
        self.tryForbiddenTransition(self.project, 'active', 'reactivate')
        self.login('employee')
        self.tryForbiddenTransition(self.project, 'active', 'close')
        self.login('customer')
        self.tryForbiddenTransition(self.project, 'active', 'close')

    def test_offer_transitions(self):
        """Test transitions of the Offer Content Type
        """
        # Manager can do all transitions on an iteration:
        self.login('manager')
        self.tryAllowedTransition(self.offer, 'offer',
                                  'private', 'publish', 'published')
        self.tryAllowedTransition(self.offer, 'offer',
                                  'published', 'retract', 'private')

        # Now try forbidden transactions for customer and employee
        self.login('customer')
        self.tryForbiddenTransition(self.offer, 'private', 'publish')
        self.login('employee')
        self.tryForbiddenTransition(self.offer, 'private', 'publish')

        self.login('manager')
        self.tryAllowedTransition(self.offer, 'offer',
                                  'private', 'publish', 'published')

        self.login('customer')
        self.tryForbiddenTransition(self.offer, 'published', 'retract')
        self.login('employee')
        self.tryForbiddenTransition(self.offer, 'published', 'retract')

    def test_iteration_transitions(self):
        """Test transitions of the Iteration Content Type
        """
        # Manager can do all transitions on an iteration:
        self.login('manager')
        self.assertEqual(self.iteration.startable(), True)
        self.assertEqual(self.story.isEstimated(), True)
        self.assertEqual(self.story.startable(), True)
        self.tryAllowedTransition(self.iteration, 'iteration',
                                  'new', 'start', 'in-progress')
        self.assertEqual(self.workflow.getInfoFor(self.story, 'review_state'),
                         'in-progress')
        self.assertEqual(self.story.completable(), False)
        self.tryAllowedTransition(self.task, 'task',
                                  'to-do', 'complete', 'completed')
        # This _should_ have automatically set the Story and the
        # Iteration to completed.
        self.assertEqual(self.story.completable(), True)
        self.assertEqual(self.workflow.getInfoFor(self.story, 'review_state'),
                         'completed')
        self.assertEqual(
            self.workflow.getInfoFor(self.iteration, 'review_state'),
            'completed')
        # Now revert
        self.tryAllowedTransition(self.iteration, 'iteration',
                                  'completed', 'reactivate', 'in-progress')
        self.tryAllowedTransition(self.iteration, 'iteration',
                                  'in-progress', 'retract', 'new')

        # Try some forbidden transactions
        self.login('customer')
        self.tryForbiddenTransition(self.iteration, 'new', 'accept')

        # Employee can only accept and complete an iteration
        self.login('employee')
        self.tryAllowedTransition(self.iteration, 'iteration',
                                  'new', 'start', 'in-progress')
        self.tryForbiddenTransition(self.iteration, 'in-progress', 'retract')
        self.tryAllowedTransition(self.iteration, 'iteration',
                                  'in-progress', 'complete', 'completed')
        self.tryForbiddenTransition(self.iteration, 'completed', 'reactivate')

        # Only a Manager can make invoicing decisions.
        self.tryForbiddenTransition(
            self.iteration, 'completed', 'no-invoicing')
        self.tryForbiddenTransition(self.iteration, 'completed', 'invoice')
        self.login('customer')
        self.tryForbiddenTransition(
            self.iteration, 'completed', 'no-invoicing')
        self.tryForbiddenTransition(self.iteration, 'completed', 'invoice')
        self.login('manager')
        self.tryAllowedTransition(self.iteration, 'iteration',
                                  'completed', 'no-invoicing', 'own-account')
        self.tryAllowedTransition(
            self.iteration, 'iteration', 'own-account', 'reconsider-invoicing',
            'completed')
        self.tryAllowedTransition(self.iteration, 'iteration',
                                  'completed', 'invoice', 'invoiced')


        # Try some transactions that don't belong to the current state
        self.tryForbiddenTransition(self.iteration, 'invoiced', 'reactivate')

    def test_story_transitions_manager(self):
        """Test transitions of the Story Content Type as Manager.
        """
        self.setRoles(['Manager'])
        # Return to initial state:
        self.tryAllowedTransition(self.story, 'story',
                                  'estimated', 'retract', 'draft')
        # There is no need for a manager to set the story to pending
        self.tryForbiddenTransition(self.story, 'draft', 'submit')
        # draft -> estimated -> draft
        self.tryAllowedTransition(self.story, 'story',
                                  'draft', 'estimate', 'estimated')
        self.tryAllowedTransition(self.story, 'story',
                                  'estimated', 'retract', 'draft')
        self.tryFullStoryRoute()

    def test_story_transitions_employee(self):
        """Test transitions of the Story Content Type as Employee.
        """
        # Return to initial state:
        self.tryAllowedTransition(self.story, 'story',
                                  'estimated', 'retract', 'draft')
        self.setRoles(['Employee'])
        self.tryFullStoryRoute()

    def test_story_transitions_customer(self):
        """Test transitions of the Story Content Type as Customer.
        """
        # Return to initial state:
        self.tryAllowedTransition(self.story, 'story',
                                  'estimated', 'retract', 'draft')
        self.setRoles(['Manager'])
        self.tryAllowedTransition(self.project, 'project',
                                  'private', 'activate', 'active')
        self.login('customer')

        # draft -> pending -> draft
        self.tryAllowedTransition(self.story, 'story',
                                  'draft', 'submit', 'pending')
        self.tryAllowedTransition(self.story, 'story',
                                  'pending', 'retract', 'draft')
        # draft -> pending -> estimated -> draft
        self.tryAllowedTransition(self.story, 'story',
                                  'draft', 'submit', 'pending')
        self.login('employee')
        self.tryAllowedTransition(self.story, 'story',
                                  'pending', 'estimate', 'estimated')
        self.login('customer')
        self.tryForbiddenTransition(self.story, 'estimated', 'activate')
        self.tryAllowedTransition(self.story, 'story',
                                  'estimated', 'retract', 'draft')

    def test_task_transitions_manager(self):
        """Test transitions of the Task Content Type as Manager.
        """
        self.setRoles(['Manager'])
        self.tryFullTaskRoute()

    def test_task_transitions_employee(self):
        """Test transitions of the Task Content Type as Employee.
        """
        self.setRoles(['Employee'])
        self.tryAllowedTransition(self.task, 'task',
                                  'open', 'activate', 'to-do')
        self.tryAllowedTransition(self.task, 'task',
                                  'to-do', 'complete', 'completed')
        self.tryAllowedTransition(self.task, 'task',
                                  'completed', 'reactivate', 'to-do')
        # Only a Manager can deactivate a Task, so an Employee can
        # not.
        self.tryForbiddenTransition(self.task, 'to-do', 'deactivate')

    def test_task_transitions_customer(self):
        """Test transitions of the Task Content Type as Customer.

        Some tests for the customer, who has no rights here:
        """
        self.twoStepTransition(self.task, 'task', 'open', 'activate',
                               'to-do', 'customer')
        self.twoStepTransition(self.task, 'task', 'to-do', 'complete',
                               'completed', 'customer')
        self.twoStepTransition(self.task, 'task', 'completed', 'reactivate',
                               'to-do', 'customer')
        self.twoStepTransition(self.task, 'task', 'to-do', 'deactivate',
                               'open', 'customer')

    def test_booking_transitions(self):
        """
        Test transitions of the Booking Content Type.
        Hm, there *aren't* any transitions here.
        """
        self.setRoles(['Manager'])
        self.tryForbiddenTransition(self.booking, 'booking', 'activate')
        self.tryForbiddenTransition(self.booking, 'booking', 'submit')

    def tryFullStoryRoute(self):
        """Test transitions of the Story Content Type
        """
        # draft -> estimated -> draft
        self.tryAllowedTransition(self.story, 'story',
                                  'draft', 'estimate', 'estimated')
        self.tryAllowedTransition(self.story, 'story',
                                  'estimated', 'retract', 'draft')

        # Set it to estimated again.
        self.tryAllowedTransition(self.story, 'story',
                                  'draft', 'estimate', 'estimated')
        # Okay, the Story is estimated.  Now it needs to be activated.
        # This can be done in two ways.

        # 1. You can activate a Story by hand.
        # estimated -> in-progress -> estimated
        self.tryAllowedTransition(self.story, 'story',
                                  'estimated', 'activate', 'in-progress')
        self.tryAllowedTransition(self.story, 'story',
                                  'in-progress', 'deactivate', 'estimated')

        # 2. You can activate a Story automatically by activating its
        # Iteration.
        self.tryAllowedTransition(self.iteration, 'iteration',
                                  'new', 'start', 'in-progress')
        self.assertEqual(self.workflow.getInfoFor(self.story, 'review_state'),
                         'in-progress')
        self.assertEqual(self.workflow.getInfoFor(self.task, 'review_state'),
                         'to-do')

        # in-progress -> completed
        # This is done automatically when all tasks of this story have
        # been completed.
        self.tryAllowedTransition(self.task, 'task',
                                  'to-do', 'complete', 'completed')
        self.assertEqual(self.workflow.getInfoFor(self.story, 'review_state'),
                         'completed')

        # completed -> in-progress
        self.tryAllowedTransition(self.story, 'story',
                                  'completed', 'improve', 'in-progress')

        # in-progress -> completed
        # The task has been completed previously, so you can now alo
        # complete the story manually.
        self.tryAllowedTransition(self.story, 'story',
                                  'in-progress', 'complete', 'completed')

    def tryAllowedTransition(self, ctObject, ctId, originalState,
                       workflowTransition, newState):
        """
        Test a transition.
        ctObject = Content Type object to perform the transition on
        ctId = id of object in the plone portal
        originalState = current state of the object
        workflowTransition = transition to perform
        newState = desired new state after the transition
        """
        self.assertEqual(self.workflow.getInfoFor(ctObject, 'review_state'),
                         originalState)
        self.workflow.doActionFor(ctObject, workflowTransition)
        self.assertEqual(self.workflow.getInfoFor(ctObject, 'review_state'),
                         newState)
        catalog = self.portal.portal_catalog
        self.failUnless(catalog(id=ctId, review_state=newState))

    def twoStepTransition(self, ctObject, ctId, originalState,
                          workflowTransition,
                          newState, loginName, useRole='Manager'):
        """
        Try a forbidden transition as user loginName.
        Then do the allowed transition as the default_user with role useRole.
        """
        self.login(loginName)
        self.tryForbiddenTransition(ctObject, originalState,
                                    workflowTransition)
        self.login(default_user)
        self.setRoles([useRole])
        self.tryAllowedTransition(ctObject, ctId, originalState,
                                  workflowTransition, newState)

    def tryFullTaskRoute(self):
        """Test transitions of the Task Content Type
        """
        self.tryAllowedTransition(self.task, 'task',
                                  'open', 'activate', 'to-do')
        self.tryAllowedTransition(self.task, 'task',
                                  'to-do', 'complete', 'completed')
        self.tryAllowedTransition(self.task, 'task',
                                  'completed', 'reactivate', 'to-do')
        self.tryAllowedTransition(self.task, 'task',
                                  'to-do', 'deactivate', 'open')

    def tryForbiddenTransition(self, ctObject, originalState,
                               workflowTransition):
        """
        Try to execute a transaction that you are not allowed to do
        ctObject = Content Type object to perform the transition on
        originalState = current state of the object
        workflowTransition = transition to perform
        """
        self.assertEqual(self.workflow.getInfoFor(ctObject, 'review_state'),
                         originalState)
        self.assertRaises(WorkflowException,
                          self.workflow.doActionFor, ctObject,
                          workflowTransition)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testWorkflow))
    return suite
