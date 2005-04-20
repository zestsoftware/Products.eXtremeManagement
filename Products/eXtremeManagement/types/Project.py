from Products.Archetypes.public import *
from Products.CMFCore import CMFCorePermissions
from AccessControl import ClassSecurityInfo
from Products.CMFCore.utils import getToolByName
from Products.eXtremeManagement.schemata import *
from Products.eXtremeManagement.config import *

from Products.Archetypes.BaseFolder import BaseFolder
from Products.Archetypes.interfaces.orderedfolder import IOrderedFolder
from Products.Archetypes import OrderedBaseFolder
from Products.Archetypes.OrderedBaseFolder import OrderedBaseFolder

schema = BaseFolderSchema + DescriptionSchema + ProjectSchema

class Project(OrderedBaseFolder):
    """A simple folderish archetype"""
    schema                = schema
    content_icon          = 'folder_icon.gif'
    meta_type             = 'Project'
    archetype_name        = 'Project'
    product_meta_type     = 'Project'
    immediate_view        = 'project_view'
    default_view          = 'project_view'
    allowed_content_types = (['Iteration', 'Story'])
    global_allow          = 0
    typeDescription       = ''
    typeDescMsgId         = ''
    security              = ClassSecurityInfo()

     
    def getMembers(self, role='Member'):
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

    def _get_project_members(self):
        """ returns a list of team members """      
        return DisplayList((self.getMembers()))

    def getProject(self):
        """ 
        returns self - useful while doing aquisition many levels down the tree 
        """
        return self


    actions = (
               {
                'id': 'view',
                'name': 'View',
                'action': 'string:${object_url}/project_view',
                'permissions': (CMFCorePermissions.View,),
                'category': 'object'
               },
              )

registerType(Project, PROJECTNAME)


