# -*- coding: utf-8 -*-
#
# File: Project.py
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
Project_schema = Project_schema +  MetadataSchema((
    BooleanField('includeGlobalMembers',
        default = True,
        languageIndependent = True,
        schemata = 'metadata', # moved to 'default' for folders
        widget = BooleanWidget(
            description="If selected, Members with a global role 'Employee' will appear in the assignees list of a Task.",
            description_msgid = "help_include_global_members",
            label = "Include global Employees",
            label_msgid = "label_include_global_members",
            i18n_domain = "eXtremeManagement",
            visible={'view' : 'hidden',
                     'edit' : 'visible'},
            ),
        ),
    ),)

Project_schema.moveField('includeGlobalMembers', pos='top')

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
    allowed_content_types = ['Iteration', 'Story', 'Folder', 'PoiTracker']
    filter_content_types = 1
    global_allow = 0
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
        get a list of all memberids that have the role ``role``
        on this project.
        """
        portal = getToolByName(self, 'portal_url').getPortalObject()

        grp = getToolByName(self, 'portal_groups')
        pu = getToolByName(self, 'plone_utils')

        memberIds=[]

        def _appendGroupsAndUsers(currentIds, extraIds):
            extraUserids = []
            for id in extraIds:
                groupdataobject = grp.getGroupById(id)
                if groupdataobject:
                    #this is a group, we need it's member ids
                    extraUserids += groupdataobject.getMemberIds()
                else:
                    #this is a member, just append it's id
                    extraUserids.append(id)
            for id in extraUserids:
                if id not in currentIds:
                    currentIds.append(id)
            return currentIds

        # member with local role ``role`` on this project
        usersandgroups = self.users_with_local_role(role)
        memberIds = _appendGroupsAndUsers(memberIds, usersandgroups)
        # members that aquired this role
        aquiredGroupsAndUsers = pu.getInheritedLocalRoles(self)
        for name, roles, type, id in aquiredGroupsAndUsers:
            if role in roles:
                if type=='user':
                    memberIds.append(id)
                elif type=='group':
                    memberIds += grp.getGroupById(id).getMemberIds()

        if self.getIncludeGlobalMembers():
            # members that have this role globally
            globalUsers = []
            if HAS_PAS:
                roleman = portal.acl_users.portal_role_manager
                for userid, loginname in roleman.listAssignedPrincipals(role):
                    globalUsers.append(userid)
            else:
               current = portal.aq_inner
               while current is not None:
                   if hasattr(current, 'aq_base') and \
                          hasattr(current.aq_base, 'acl_users'):
                       for user in current.acl_users.getUsers():
                           if role in user.getRoles():
                               globalUsers.append(user.getId())
                   current = getattr(current, 'aq_parent', None)
            memberIds = _appendGroupsAndUsers(memberIds, globalUsers)

        return memberIds

    security.declarePublic('currentIteration')
    def currentIteration(self):
        """Return the currently in-progress iteration.

        If two iterations are in-progress, for now return the first
        one.
        """
        catalog = getToolByName(self, 'portal_catalog')
        searchpath = '/'.join(self.getPhysicalPath())
        iterations = catalog.searchResults(
            portal_type='Iteration',
            review_state='in-progress',
            path=searchpath)
        if len(iterations) == 0:
            return None
        else:
            return iterations[0].getObject()


registerType(Project, PROJECTNAME)
# end of class Project

##code-section module-footer #fill in your manual code here
##/code-section module-footer



