from Products.Archetypes.public import *
from Products.CMFCore import CMFCorePermissions
from AccessControl import ClassSecurityInfo
from Products.CMFCore.utils import getToolByName
from Products.eXtremeManagement.schemata import *
from Products.eXtremeManagement.config import *

schema = BaseFolderSchema + TaskSchema 

class Task(BaseContent):
    """A simple archetype"""
    schema                = schema
    content_icon          = 'document_icon.gif'
    meta_type             = 'Task'
    archetype_name        = 'Task'
    product_meta_type     = 'Task'
    immediate_view        = 'base_view'
    default_view          = 'base_view'
    allowed_content_types = ([])
    global_allow          = 0
    typeDescription       = ''
    typeDescMsgId         = ''
    security              = ClassSecurityInfo()


    def _get_hours_vocab(self):
        props = self.portal_properties.extreme_properties
        return props.getProperty('hours')

    def _get_minutes_vocab(self):
        props = self.portal_properties.extreme_properties
        return props.getProperty('minutes')

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
    
    def _get_assignees(self):
        """ returns a list of team members """
        return DisplayList((self.getProject().getMembers()))


    actions = (
               {
                'id': 'view',
                'name': 'View',
                'action': 'string:${object_url}/base_view',
                'permissions': (CMFCorePermissions.View,),
                'category': 'object'
               },
              )

registerType(Task, PROJECTNAME)


