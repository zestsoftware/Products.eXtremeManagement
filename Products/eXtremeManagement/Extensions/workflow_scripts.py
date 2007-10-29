from Products.CMFCore.utils import getToolByName
from types import StringTypes
import logging

from xm.booking.timing.interfaces import IEstimate

##########################
# Task Workflow scripts #
#########################

def emailContact(portal, memberid, allowPortalContact=False):
    membership = getToolByName(portal, 'portal_membership')
    member = membership.getMemberById(memberid)
    if member is None:
        # Maybe a test user?
        return ''

    email = member.getProperty('email', None)
    if email == '' or email is None:
        if allowPortalContact:
            email = portal.getProperty('email_from_address',
                                       'postmaster@localhost')
        else:
            return ''

    fullname = member.getProperty('fullname', None)
    if fullname == '' or fullname is None:
        if allowPortalContact:
            fullname = portal.getProperty('email_from_name', None)
        else:
            fullname = 'Fullname unknown'

    emailContact = '%s <%s>' % (fullname, email)
    return emailContact

def mailMessage(portal, obj, subject, destination=None, log=None):
    """
    Mail a message in reaction to a transition.
    Thanks to Alan Runyan.  Adapted from:
    http://plone.org/documentation/how-to/send-mail-on-workflow-transition

    If destination is not None, then only mail to destination, which
    should be just 1 person.
    """
    if log is None:
        # FIXME: defining log here doesn't seem to be working
        log = logging.getLogger("eXtremeManagement Task mail")
    if destination is not None and not isinstance(destination, StringTypes):
        log.warn('destination should be a string, but is %s.', destination)
        return
    else:
        log.info('Will mail to destination=%s.', destination)

    membership = getToolByName(portal, 'portal_membership')
    wf_tool = getToolByName(portal, 'portal_workflow')
    mailhost = getToolByName(portal, 'MailHost')
    # This is the original creator of the task:
    creatorid = obj.Creator()

    mMsg = """
The url is:
%s

The original creator of this task is:
%s

%s

This estimate for this task is currently: %s hours.

This task is assigned to:
%s

You can do it!
"""
    mTitle = obj.Title()
    mSubj = '%s: %s' % (subject, mTitle)
    obj_url = obj.absolute_url() #use portal_url + relative_url
    mCreator = emailContact(portal, creatorid, allowPortalContact=True)
    mFrom = mCreator

    # These are the persons that this task is now assigned to:
    assignees = obj.getAssignees()
    listofAssignees = ''
    for assignee in assignees:
        listofAssignees += emailContact(portal, assignee)
        listofAssignees += '\n'

    description = obj.Description()
    if description != '':
        description = 'The description of the task is:' + description

    estimate = IEstimate(obj, None)
    if estimate is not None:
        estimate = estimate.hours
    message = mMsg % (obj_url, mCreator, description,
                      estimate, listofAssignees)
    if destination:
        assignees = [destination]
    for assignee in assignees:
        mTo = emailContact(portal, assignee)
        # If email address is known:
        if mTo and mTo != '' and mTo != mCreator:
            try:
                mailhost.simple_send(mTo, mFrom, mSubj, message)
            except:
                log.warn('Mailing to %s failed.', mTo)
    return True

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
        review_state = wf_tool.getInfoFor(task,'review_state')
        if review_state == 'open':
            try:
                wf_tool.doActionFor(task, 'activate')
            except WorkflowException:
                print 'ERROR: task %s with status %s in story %s can not be activated!.' \
                      % (task.Title(), review_state, story.Title())

def tryToCompleteIteration(self, state_change, **kw):
    """
    If all Stories in an Iteration have been set to complete, then the
    Iteration itself can be set to complete.  Try that.
    """
    portal = self
    story=state_change.object
    iteration = story.aq_parent
    wf_tool = getToolByName(portal, 'portal_workflow')
    from Products.CMFCore.WorkflowCore import WorkflowException
    try:
        wf_tool.doActionFor(iteration, 'complete')
    except WorkflowException:
        pass

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
        review_state = wf_tool.getInfoFor(story,'review_state')
        if review_state == 'estimated':
            try:
                wf_tool.doActionFor(story, 'activate')
            except WorkflowException:
                print 'WARNING: story %s with status %s in iteration %s can not be activated..' \
                      % (story.Title(), review_state, iteration.Title())
