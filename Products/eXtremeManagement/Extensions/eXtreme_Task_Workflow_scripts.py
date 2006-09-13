# -*- coding: utf-8 -*-
#
# File: eXtremeManagement.py
#
# Copyright (c) 2006 by Zest software, Lovely Systems
# Generator: ArchGenXML Version 1.5.0 svn/devel
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

__author__ = """Ahmad Hadi <a.hadi@zestsoftware.nl>, Maurits van Rees
<m.van.rees@zestsoftware.nl>, Jodok Batlogg <jodok.batlogg@lovelysystems.com>"""
__docformat__ = 'plaintext'


# Workflow Scripts for: eXtreme_Task_Workflow

##code-section workflow-script-header #fill in your manual code here

from Products.CMFCore.utils import getToolByName
from types import StringTypes
import logging


def emailContact(portal, memberid, allowPortalContact=False):
    membership = getToolByName(portal, 'portal_membership')
    member = membership.getMemberById(memberid)

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
    """Mail a message in reaction to a transition.

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
        description = """The description of the task is:
""" + description

    message = mMsg % (obj_url, mCreator, description,
                      obj.getEstimate(), listofAssignees)

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

##/code-section workflow-script-header


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

