# -*- coding: utf-8 -*-
#
# File: Project.py
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
import string

##/code-section module-header

schema = Schema((

),
)

##code-section after-local-schema #fill in your manual code here

OrderedBaseFolderSchema = OrderedBaseFolderSchema.copy()
OrderedBaseFolderSchema['description'].isMetadata = False
OrderedBaseFolderSchema['description'].schemata = 'default'

##/code-section after-local-schema

Project_schema = OrderedBaseFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Project(OrderedBaseFolder):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(OrderedBaseFolder,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Project'

    meta_type = 'Project'
    portal_type = 'Project'
    allowed_content_types = ['Iteration', 'Story', 'PoiTracker']
    filter_content_types = 1
    global_allow = 1
    content_icon = 'project_icon.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "Project"
    typeDescMsgId = 'description_edit_project'


    actions =  (


       {'action': "string:${object_url}/project_team",
        'category': "object",
        'id': 'team',
        'name': 'Projectteam',
        'permissions': ("View",),
        'condition': 'python:1'
       },


    )

    _at_rename_after_creation = True

    schema = Project_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('getProject')
    def getProject(self):
        """
        returns self - useful while doing aquisition many levels down the tree
        """
        return self

    security.declarePublic('getMembers')
    def getMembers(self, role='Employee'):
        """
        """
        grp = getToolByName(self, 'portal_groups')
        mem = getToolByName(self, 'portal_membership')
        # PAS doesn't use prefixes at all
        # TODO: probably we want a global switch for PAS
        try:
            import Products.PlonePAS
        except ImportError:
            prefix=self.acl_users.getGroupPrefix()
        else:
            prefix=''
        list1 = []
        for user, roles in self.get_local_roles():
            if role in roles:
                if prefix != '' and string.find(user, prefix) == 0:
                    for i1 in grp.getGroupById(user).getGroupMembers():
                        list1.append(i1.getId())
                else:
                    m1 = mem.getMemberById(user)
                    if m1:
                        list1.append(m1.getId())

        return list1


registerType(Project, PROJECTNAME)
# end of class Project

##code-section module-footer #fill in your manual code here
##/code-section module-footer



