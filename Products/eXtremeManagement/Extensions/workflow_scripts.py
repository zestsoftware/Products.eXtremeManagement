import logging

import transaction
from Products.CMFCore.utils import getToolByName

logger = logging.getLogger("eXtremeManagement workflow scripts")


##########################
# Task Workflow scripts #
#########################


def notify_completed(self, state_change, **kw):
    """
    Notify interested people that a task has been completed.

    Has been disabled at the moment.
    """
    portal = self
    obj=state_change.object


def tryToCompleteStory(self, state_change, **kw):
    portal = self
    task=state_change.object
    story = task.aq_parent
    wf_tool = getToolByName(portal, 'portal_workflow')
    from Products.CMFCore.WorkflowCore import WorkflowException
    try:
        wf_tool.doActionFor(story, 'complete')
    except WorkflowException:
        pass


def improve_story(self, state_change, **kw):
    """
    Notify interested people that a task has been completed.

    Has been disabled at the moment.
    """
    story = state_change.object.aq_parent
    wf_tool = getToolByName(self, 'portal_workflow')
    state = wf_tool.getInfoFor(story, 'review_state')
    if state == 'completed':
        from Products.CMFCore.WorkflowCore import WorkflowException
        try:
            wf_tool.doActionFor(story, 'improve')
        except WorkflowException:
            pass


##########################
# Story Workflow scripts #
##########################


def startStory(self, state_change, **kw):
    """
    Give all open tasks in this story the to-do status.
    """
    portal = self
    story=state_change.object
    # Tasks have statuses open, to-do or completed.
    # Open tasks need to be set to to-do.  The rest is fine.
    tasks = story.contentValues(filter={'portal_type': ['Task', 'PoiTask']})
    wf_tool = getToolByName(portal, 'portal_workflow')
    from Products.CMFCore.WorkflowCore import WorkflowException
    for task in tasks:
        review_state = wf_tool.getInfoFor(task, 'review_state')
        if review_state == 'open':
            try:
                wf_tool.doActionFor(task, 'activate')
                logger.debug('Activated task %s', task)
                transaction.savepoint()
            except WorkflowException:
                logger.error(
                    "Task %s with status %s in story %s can not be activated!"
                    % (task.Title(), review_state, story.Title()))


def tryToCompleteIteration(self, state_change, **kw):
    """
    If all Stories in an Iteration have been set to complete, then the
    Iteration itself can be set to complete.  Try that.
    """
    portal = self
    story=state_change.object
    iteration = story.aq_parent
    wf_tool = getToolByName(portal, 'portal_workflow')
    if wf_tool.getInfoFor(iteration, 'review_state') == 'in-progress' and \
            iteration.completable():
        wf_tool.doActionFor(iteration, 'complete')

##############################
# Iteration Workflow scripts #
##############################


def startIteration(self, state_change, **kw):
    """
    Give all estimated stories in this iteration the in-progress status.
    """
    portal = self
    iteration=state_change.object
    stories = iteration.contentValues(filter={'portal_type': 'Story'})
    wf_tool = getToolByName(portal, 'portal_workflow')
    from Products.CMFCore.WorkflowCore import WorkflowException
    for story in stories:
        review_state = wf_tool.getInfoFor(story, 'review_state')
        if review_state == 'estimated':
            try:
                wf_tool.doActionFor(story, 'activate')
                logger.debug('Activated story %s', story)
                transaction.savepoint()
            except WorkflowException:
                logger.warn("Story %s with status %s in iteration %s can "
                            "not be activated." % (story.Title(),
                                                   review_state,
                                                   iteration.Title()))
