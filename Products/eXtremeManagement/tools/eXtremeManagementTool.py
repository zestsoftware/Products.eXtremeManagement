# -*- coding: utf-8 -*-
#
# File: eXtremeManagementTool.py
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


from Products.CMFCore.utils import UniqueObject

    
##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

eXtremeManagementTool_schema = BaseSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class eXtremeManagementTool(UniqueObject, BaseContent):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(UniqueObject,'__implements__',()),) + (getattr(BaseContent,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'eXtremeManagementTool'

    meta_type = 'eXtremeManagementTool'
    portal_type = 'eXtremeManagementTool'
    allowed_content_types = []
    filter_content_types = 0
    global_allow = 0
    allow_discussion = False
    #content_icon = 'eXtremeManagementTool.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "eXtremeManagementTool"
    typeDescMsgId = 'description_edit_extrememanagementtool'
    #toolicon = 'eXtremeManagementTool.gif'

    _at_rename_after_creation = True

    schema = eXtremeManagementTool_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header


    # tool-constructors have no id argument, the id is fixed
    def __init__(self, id=None):
        BaseContent.__init__(self,'xm_tool')
        self.setTitle('eXtremeManagementTool')
        
        ##code-section constructor-footer #fill in your manual code here
        ##/code-section constructor-footer


    # Methods

    security.declarePublic('formatTime')
    def formatTime(self,time):
        """
        Returns time as a formatted string
        e.g. 3:15
        """
        hours = int(time)        
        minutes = int(round((time - hours)*60))
        # Adjust for rounding:
        if minutes == 60:
            minutes = 0
            hours += 1
        if hours == 0 and minutes == 0:
            return ('0:00')
        minutes = abs(minutes)
        hours = abs(hours)
        minutes = self.formatMinutes(minutes)
        # This should not happen:
        if minutes is False:
            minutes = ':ERROR'
        sign = ''
        if time < 0:
            sign = '-'
        return ('%s%s%s' % (sign, hours, minutes))

    security.declarePublic('formatMinutes')
    def formatMinutes(self,minutes):
        """
        Takes the integer argument minutes and formats it nicely.  Examples:
        5  => :05
        24 => :24
        minutes should be between 0 and 59.
        """
        minutes = int(minutes)
        if minutes < 0:
            return False
        if minutes > 59:
            return False
        if minutes < 10:
            minutes = '0%s' % minutes
        minutes = ':%s' % minutes
        return minutes

    security.declarePublic('getProjectsToList')
    def getProjectsToList(self):
        """
        return all projects for the current user
        """
        pc = getToolByName(self, 'portal_catalog')
        brains = pc({'portal_type': 'Project', 'review_state': 'active'})
        for brain in brains:
            projects.append(brain.getObject())

        return projects

    security.declarePublic('getIssues')
    def getFilteredIssues(self, filter={}):
        """
        return issues (POI) that match the given filter.
    
        filter is a dictionary containing portal_catalog queries, eg:
            
        * filter = {} -> all issues are returned
        * filter = {'state': ['open','unconfirmed']} -> all
          open or unconfirmed issues are returned
        
        returs:
        { {'title':'issues for me', 'issues':[issue1,...]}, {'title':'issues from me', 'issues':[issue1,...]} } 
        """
        pc = getToolByName(self, 'portal_catalog')
        mtool = getToolByName(self, 'portal_membership')

        currentUser = mtool.getAuthenticatedMember().getId()

        grouped_issues = []

        # issues assigned to me
        issue_group = {'title': 'Issues assigned to me'}
        grouped_issues.append(issue_group)
        
        searchFilter = filter
        searchFilter['portal_type'] = 'PoiIssue'
        searchFilter['getResponsibleManager'] = currentUser
        
        issue_group['issues'] = pc(searchFilter)

        # issues created by me
        issue_group = {'title': 'Issues created by me'}
        grouped_issues.append(issue_group)
        
        searchFilter = filter
        searchFilter['portal_type'] = 'PoiIssue'
        searchFilter['Creator'] = currentUser
        
        issue_group['issues'] = pc(searchFilter)

        return grouped_issues

registerType(eXtremeManagementTool, PROJECTNAME)
# end of class eXtremeManagementTool

##code-section module-footer #fill in your manual code here
##/code-section module-footer



