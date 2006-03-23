# -*- coding: utf-8 -*-
#
# File: ProjectFolder.py
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
##/code-section module-header

schema = Schema((

),
)

##code-section after-local-schema #fill in your manual code here

OrderedBaseFolderSchema = OrderedBaseFolderSchema.copy()
OrderedBaseFolderSchema['description'].isMetadata = False
OrderedBaseFolderSchema['description'].schemata = 'default'

##/code-section after-local-schema

ProjectFolder_schema = OrderedBaseFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class ProjectFolder(OrderedBaseFolder):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(OrderedBaseFolder,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'ProjectFolder'

    meta_type = 'ProjectFolder'
    portal_type = 'ProjectFolder'
    allowed_content_types = ['Project']
    filter_content_types = 1
    global_allow = 1
    content_icon = 'project_icon.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "ProjectFolder"
    typeDescMsgId = 'description_edit_projectfolder'


    actions =  (


       {'action': "string:${object_url}/project_listing",
        'category': "object",
        'id': 'view',
        'name': 'view',
        'permissions': ("View",),
        'condition': 'python:1'
       },


    )

    _at_rename_after_creation = True

    schema = ProjectFolder_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('formatTime')
    def formatTime(self, time):
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
    def formatMinutes(self, minutes):
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


registerType(ProjectFolder, PROJECTNAME)
# end of class ProjectFolder

##code-section module-footer #fill in your manual code here
##/code-section module-footer



