# File: Project.py
# 
# Copyright (c) 2005 by ['']
# Generator: ArchGenXML Version 1.4.0-beta2 http://sf.net/projects/archetypes/
#
# GNU General Public Licence (GPL)
# 
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place, Suite 330, Boston, MA  02111-1307  USA
#
__author__  = ''' <>'''
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *




from Products.eXtremeManagement.config import *
##code-section module-header #fill in your manual code here

BaseFolderSchema = OrderedBaseFolderSchema.copy()
BaseFolderSchema['description'].isMetadata = False
BaseFolderSchema['description'].schemata = 'default'

##/code-section module-header

schema=Schema((
),
)


##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Project(OrderedBaseFolder,BaseFolder):
    security = ClassSecurityInfo()
    __implements__ = (getattr(OrderedBaseFolder,'__implements__',()),) + (getattr(BaseFolder,'__implements__',()),)


    # This name appears in the 'add' box
    archetype_name             = 'Project'

    meta_type                  = 'Project' 
    portal_type                = 'Project' 
    allowed_content_types      = ['Iteration', 'Story'] + list(getattr(OrderedBaseFolder, 'allowed_content_types', []))
    filter_content_types       = 1
    global_allow               = 0
    allow_discussion           = 0
    #content_icon               = 'Project.gif'
    immediate_view             = 'base_view'
    default_view               = 'base_view'
    typeDescription            = "Project"
    typeDescMsgId              = 'description_edit_project'

    schema = BaseFolderSchema + \
             getattr(OrderedBaseFolder,'schema',Schema(())) + \
             schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header


    #Methods

    security.declarePublic('getProject')
    def getProject(self):
        """
        returns self - useful while doing aquisition many levels down the tree
        """
        return self


    security.declarePublic('getMembers')
    def getMembers(self):
        """
        """
        grp = getToolByName(self, 'portal_groups')
        mem = getToolByName(self, 'portal_membership')
        prefix=self.acl_users.getGroupPrefix()
        list1 = []
        for user, roles in self.get_local_roles():
            if role in roles:
                if string.find(user, prefix) == 0:
                    for i1 in grp.getGroupById(user).getGroupMembers():
                        name = hasattr(i1, 'fullname') and i1.fullname.strip() or i1.getId()
                        list1.append((i1.getId(), name))
                else:
                    m1 = mem.getMemberById(user)
                    if m1:
                        id = m1.getId()
                        name = hasattr(m1, 'fullname') and m1.fullname.strip() or m1.getId()
                    else:
                        id = name = user
                    list1.append((id, name))

        return list1


registerType(Project,PROJECTNAME)
# end of class Project

##code-section module-footer #fill in your manual code here
##/code-section module-footer



