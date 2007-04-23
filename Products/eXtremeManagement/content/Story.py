# -*- coding: utf-8 -*-
#
# File: Story.py
#
# Copyright (c) 2006 by Zest software, Lovely Systems
# Generator: ArchGenXML 
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

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.eXtremeManagement.config import *

##code-section module-header #fill in your manual code here
from zope.interface import implements
from Products.eXtremeManagement.interfaces import IXMStory

from Products.CMFCore.utils import getToolByName
BaseFolderSchema = OrderedBaseFolderSchema.copy()
BaseFolderSchema['id'].widget.visible = {'edit':'hidden', 'view':'invisible'}

##/code-section module-header

schema = Schema((

    TextField(
        name='mainText',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        widget=RichWidget(
            description="Enter the main description for this object.",
            label='Main text',
            label_msgid='eXtremeManagement_label_mainText',
            description_msgid='eXtremeManagement_help_mainText',
            i18n_domain='eXtremeManagement',
        ),
        default_output_type='text/html',
        required=1
    ),

    FloatField(
        name='roughEstimate',
        widget=DecimalWidget(
            description="Enter a rough estimate in days (tip: use multiples of 0.5 days)",
            label='Rough estimate',
            label_msgid='eXtremeManagement_label_roughEstimate',
            description_msgid='eXtremeManagement_help_roughEstimate',
            i18n_domain='eXtremeManagement',
        ),
        write_permission="eXtremeManagement: Edit roughEstimate",
        validators=('isDecimal',)
    ),

),
)


Story_schema = OrderedBaseFolderSchema.copy() + \
    schema.copy()


class Story(OrderedBaseFolder):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(OrderedBaseFolder,'__implements__',()),)
    implements(IXMStory)

    # This name appears in the 'add' box
    archetype_name = 'Story'

    meta_type = 'Story'
    portal_type = 'Story'
    allowed_content_types = ['Task']
    filter_content_types = 1
    global_allow = 0
    content_icon = 'story_icon.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "Story"
    typeDescMsgId = 'description_edit_story'
    allow_discussion = True

    _at_rename_after_creation = True

    schema = Story_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('CookedBody')
    def CookedBody(self):
        """
        Dummy attribute to allow drop-in replacement of Document
        """
        return self.getMainText()

    security.declarePublic('get_progress_perc')
    def get_progress_perc(self):
        """
        When a story is completed, the progress is 100% by definition.
        """
        if self.isCompleted():
            return 100
        else:
            xt = getToolByName(self, 'xm_tool')
            estimated = self.getRawEstimate()
            actual = self.getRawActualHours()
            return xt.get_progress_perc(actual, estimated)
        

    security.declarePublic('generateUniqueId')
    def generateUniqueId(self, type_name):
        """ Generate sequential IDs for tasks
        With thanks to Upfront Systems for their code from Upfront Project
        """
        if type_name == 'Task':
            tasks = self.getStoryTasks()
            taskids = [0]
            for task in tasks:
                try:
                    taskid = task.getId()
                    taskids.append(int(taskid))
                except:
                    print 'WARNING: non-integer taskid found: %s' % taskid
            lastTaskId = max(taskids) + 1
            return str(lastTaskId)
        else:
            return self.aq_parent.generateUniqueId(type_name)

    security.declarePublic('isCompleted')
    def isCompleted(self):
        """
        Returns True is the Story has review_state 'completed'.
        """
        portal = getToolByName(self,'portal_url').getPortalObject()
        wf_tool = getToolByName(portal, 'portal_workflow')
        state = wf_tool.getInfoFor(self, 'review_state')
        if state == 'completed':
            return True
        else:
            return False

    security.declarePublic('getRawEstimate')
    def getRawEstimate(self):
        """
        When a story has tasks, get their estimates.
        If not, get the roughEstimate of this story.
        HOURS_PER_DAY is set in AppConfig.py (probably 8).
        """


        tasks = self.getStoryTasks()
        estimated = 0.0
        estimates = []
        if tasks:
            for task in tasks:
                estimates.append(task.getRawEstimate())
            estimated = sum(estimates)
        if estimated == 0:
            try:
                estimated = self.getRoughEstimate() * HOURS_PER_DAY
            except:
                estimated = 0
        return estimated

    security.declarePublic('getEstimate')
    def getEstimate(self):
        """

        """
        xt = getToolByName(self, 'xm_tool')
        return xt.formatTime(self.getRawEstimate())

    security.declarePublic('getRawActualHours')
    def getRawActualHours(self):
        """

        """
        tasks = self.getStoryTasks()
        actual = 0.0
        if tasks:
            for task in tasks:
                actual = actual + task.getRawActualHours()
        return actual

    security.declarePublic('getActualHours')
    def getActualHours(self):
        """

        """
        xt = getToolByName(self, 'xm_tool')
        return xt.formatTime(self.getRawActualHours())

    security.declarePublic('getRawDifference')
    def getRawDifference(self):
        """

        """
        return self.getRawActualHours() -  self.getRawEstimate()

    security.declarePublic('getDifference')
    def getDifference(self):
        """

        """
        xt = getToolByName(self, 'xm_tool')
        return xt.formatTime(self.getRawDifference())

    security.declarePublic('isEstimated')
    def isEstimated(self):
        """
        True when roughEstimate is set.  Actually, it could be an old
        Story which does not have a roughEstimate.  That is okay, as
        long as the story has tasks that have an estimate.  The
        roughEstimate is superfluous in that case.  So checking the
        raw estimate is good.
        """
        if self.getRawEstimate() > 0:
            return True
        else:
            return False

    security.declarePublic('startable')
    def startable(self):
        """
        Test if all tasks in this story can be activated and if the
        Story itself has been estimated.  If the story is somehow
        already in-progress or completed, then that is fine as well.
        """
        unAcceptableStatuses = ['draft','pending']
        portal = getToolByName(self,'portal_url').getPortalObject()
        wf_tool = getToolByName(portal, 'portal_workflow')
        review_state = wf_tool.getInfoFor(self,'review_state')
        if review_state in unAcceptableStatuses:
            return False
        if not self.isEstimated():
            return False
        tasks = self.getStoryTasks()
        if not tasks:
            return False
        else:
            for task in tasks:
                if not task.startable():
                    return False
            return True

    security.declarePublic('completable')
    def completable(self):
        """
        Test if all tasks in this iteration have completed.
        """
        portal = getToolByName(self,'portal_url').getPortalObject()
        wf_tool = getToolByName(portal, 'portal_workflow')
        tasks = self.getStoryTasks()
        for task in tasks:
            review_state = wf_tool.getInfoFor(task,'review_state')
            if review_state != 'completed':
                return False
        return True

    # Manually created methods

    security.declarePublic('getStoryTasks')
    def getStoryTasks(self):
        """return the tasks of this story
        """
        return self.contentValues(filter={'portal_type': 'Task'})

    def _delObject(self, orig_id, *args, **kwargs):
        super(Story, self)._delObject(orig_id, *args, **kwargs)
        self.reindexObject()

registerType(Story, PROJECTNAME)
# end of class Story

##code-section module-footer #fill in your manual code here
##/code-section module-footer



