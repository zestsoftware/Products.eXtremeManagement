from Products.Archetypes.public import *
from Products.CMFCore import CMFCorePermissions
from AccessControl import ClassSecurityInfo
from Products.eXtremeManagement.schemata import *
from Products.eXtremeManagement.config import *

schema = BaseFolderSchema 

class ProjectMember(BaseContent):
    """A simple archetype"""
    schema                = schema
    content_icon          = 'user.gif'
    meta_type             = 'ProjectMember'
    archetype_name        = 'ProjectMember'
    product_meta_type     = 'ProjectMember'
    immediate_view        = 'project_member_view'
    default_view          = 'project_member_view'
    allowed_content_types = ([])
    global_allow          = 0
    typeDescription       = ''
    typeDescMsgId         = ''
    security              = ClassSecurityInfo()

    actions = (
               {
                'id': 'view',
                'name': 'View',
                'action': 'string:${object_url}/project_member_view',
                'permissions': (CMFCorePermissions.View,),
                'category': 'object'
               },
              )

registerType(ProjectMember, PROJECTNAME)


