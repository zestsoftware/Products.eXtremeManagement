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


# Workflow Scripts for: eXtreme_Story_Workflow

##code-section workflow-script-header #fill in your manual code here
from Products.CMFCore.utils import getToolByName
##/code-section workflow-script-header


def startStory(self, state_change, **kw):
    """
    Give all open tasks in this story the to-do status.
    """
    portal = self
    story=state_change.object
    # Tasks have statuses open, to-do or completed.
    # Open tasks need to be set to to-do.  The rest is fine.
    tasks = story.contentValues('Task')
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


