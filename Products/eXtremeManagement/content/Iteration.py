# -*- coding: utf-8 -*-
#
# File: Iteration.py
#
# Copyright (c) 2006 by Zest software
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
<m.van.rees@zestsoftware.nl>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.eXtremeManagement.config import *

##code-section module-header #fill in your manual code here
from Products.CMFCore.utils import getToolByName
##/code-section module-header

schema = Schema((

    DateTimeField(
        name='startDate',
        widget=CalendarWidget(
            show_hm=False,
            label='Startdate',
            label_msgid='eXtremeManagement_label_startDate',
            i18n_domain='eXtremeManagement',
        )
    ),

    DateTimeField(
        name='endDate',
        widget=CalendarWidget(
            show_hm=False,
            label='Enddate',
            label_msgid='eXtremeManagement_label_endDate',
            i18n_domain='eXtremeManagement',
        )
    ),

    IntegerField(
        name='manHours',
        widget=IntegerWidget(
            label='Manhours',
            label_msgid='eXtremeManagement_label_manHours',
            i18n_domain='eXtremeManagement',
        )
    ),

),
)

##code-section after-local-schema #fill in your manual code here

OrderedBaseFolderSchema = OrderedBaseFolderSchema.copy()
OrderedBaseFolderSchema['description'].isMetadata = False
OrderedBaseFolderSchema['description'].schemata = 'default'

##/code-section after-local-schema

Iteration_schema = OrderedBaseFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Iteration(OrderedBaseFolder):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(OrderedBaseFolder,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Iteration'

    meta_type = 'Iteration'
    portal_type = 'Iteration'
    allowed_content_types = ['Story']
    filter_content_types = 1
    global_allow = 0
    content_icon = 'iteration_icon.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "Iteration"
    typeDescMsgId = 'description_edit_iteration'

    _at_rename_after_creation = True

    schema = Iteration_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('getRawEstimate')
    def getRawEstimate(self):
        """

        """
        stories = self.contentValues()
        estimated = 0.0
        estimates = []
        if stories:
            for story in stories:
                estimates.append(story.getRawEstimate())
            estimated = sum(estimates)
        return estimated

    security.declarePublic('getEstimate')
    def getEstimate(self):
        """

        """
        return self.formatTime(self.getRawEstimate())

    security.declarePublic('getRawActualHours')
    def getRawActualHours(self):
        """

        """
        stories = self.contentValues()
        actual = 0.0
        if stories:
            for story in stories:
                actual = actual + story.getRawActualHours()
        return actual

    security.declarePublic('getActualHours')
    def getActualHours(self):
        """

        """
        return self.formatTime(self.getRawActualHours())

    security.declarePublic('getRawDifference')
    def getRawDifference(self):
        """

        """
        return self.getRawActualHours() -  self.getRawEstimate()

    security.declarePublic('getDifference')
    def getDifference(self):
        """

        """
        return self.formatTime(self.getRawDifference())

    security.declarePublic('startable')
    def startable(self):
        """
        Test if all stories in this iteration have statuses that are
        okay.  Usually that status should be 'estimated', but at least
        it should not be 'draft' or 'pending'.
        """
        unAcceptableStatuses = ['draft','pending']
        portal = getToolByName(self,'portal_url').getPortalObject()
        wf_tool = getToolByName(portal, 'portal_workflow')
        stories = self.contentValues('Story')
        for story in stories:
            review_state = wf_tool.getInfoFor(story,'review_state')
            if review_state in unAcceptableStatuses:
                return False
        return True

    security.declarePublic('completable')
    def completable(self):
        """
        Test if all stories in this iteration have completed.
        """
        portal = getToolByName(self,'portal_url').getPortalObject()
        wf_tool = getToolByName(portal, 'portal_workflow')
        stories = self.contentValues('Story')
        for story in stories:
            review_state = wf_tool.getInfoFor(story,'review_state')
            if review_state != 'completed':
                return False
        return True


registerType(Iteration, PROJECTNAME)
# end of class Iteration

##code-section module-footer #fill in your manual code here
##/code-section module-footer



