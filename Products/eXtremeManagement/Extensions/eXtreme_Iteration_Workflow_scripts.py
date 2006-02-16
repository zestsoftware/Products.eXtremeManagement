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


# Workflow Scripts for: eXtreme_Iteration_Workflow

##code-section workflow-script-header #fill in your manual code here
from Products.CMFCore.utils import getToolByName
##/code-section workflow-script-header


def startIteration(self, state_change, **kw):
    """
    Give all estimated stories in this iteration the in-progress status.
    """
    portal = self
    iteration=state_change.object
    stories = iteration.contentValues('Story')
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

