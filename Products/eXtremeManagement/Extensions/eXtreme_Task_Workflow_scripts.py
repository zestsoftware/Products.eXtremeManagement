# File: eXtremeManagement.py
#
# Copyright (c) 2006 by Zest software
# Generator: ArchGenXML Version 1.4.1 svn/devel
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
<m.van.rees@zestsoftware.nl>"""
__docformat__ = 'plaintext'


# Workflow Scripts for: eXtreme_Task_Workflow

##code-section workflow-script-header #fill in your manual code here

from Products.CMFCore.utils import getToolByName


def emailContact(portal, memberid, allowPortalContact=False):
    membership = getToolByName(portal, 'portal_membership')
    member = membership.getMemberById(memberid)

    email = member.getProperty('email', None)
    if email == '' or email is None:
        if allowPortalContact:
            email = portal.getProperty('email_from_address',
                                       'postmaster@localhost')
        else:
            return None

    fullname = member.getProperty('fullname', None)
    if fullname == '' or fullname is None:
        if allowPortalContact:
            fullname = portal.getProperty('email_from_name', None)
        else:
            fullname = 'Fullname unknown'

    emailContact = '%s <%s>' % (fullname, email)
    return emailContact

##/code-section workflow-script-header


def notify_assignees(self, state_change, **kw):
    """
    Thanks to Alan Runyan.  Adapted from:
    http://plone.org/documentation/how-to/send-mail-on-workflow-transition
    """

    obj=state_change.object
    history = state_change.getHistory()

    portal = getToolByName(self,'portal_url').getPortalObject()
    membership = getToolByName(portal, 'portal_membership')
    wf_tool = getToolByName(portal, 'portal_workflow')
    mailhost = getToolByName(portal, 'MailHost')

    # This is the original creator of the task:
    creatorid = obj.Creator()
    
    # This is the person that assigned this task to someone:
    actorid = wf_tool.getInfoFor(obj, 'actor')
    mFrom = emailContact(portal, actorid, allowPortalContact=True)
    if mFrom is None:
        return False
    
    mMsg = """
The url is:
%s.

The original creator of this task is:
%s

The description of the task is:
%s

This task is estimated at: %s hours.

This task has been assigned to:
%s

This task has been assigned by:
%s

"""

    mTitle = obj.Title()
    mSubj = 'You have a new task: %s' % mTitle
    obj_url = obj.absolute_url() #use portal_url + relative_url
    #comments = wf_tool.getInfoFor(obj, 'comments')
    mCreator = emailContact(portal, creatorid, allowPortalContact=True)
    mFrom = emailContact(portal, actorid, allowPortalContact=True)
    mInitializer = emailContact(portal, actorid)
    if mInitializer is None or mInitializer == '':
        mInitializer = 'unknown'
    # These are the persons that this task is now assigned to:
    assignees = obj.getAssignees()
    listofAssignees = ''
    for assignee in assignees:
        listofAssignees += emailContact(portal, assignee)
        listofAssignees += '\n'


    message = mMsg % (obj_url, mCreator, obj.Description(),
                      obj.getEstimate(), listofAssignees,
                      mInitializer)


    for assignee in assignees:
        mTo = emailContact(portal, assignee)
        if mTo:
            try:
                mailhost.simple_send(mTo, mFrom, mSubj, message)
            except:
                return False
        else:
            return False

    # Send email to initializer:
    mSubj = 'You have assigned a new task: %s' % mTitle
    if mInitializer and mInitializer != 'unknown':
        mailhost.simple_send(mInitializer, mFrom, mSubj, message)

    return True
