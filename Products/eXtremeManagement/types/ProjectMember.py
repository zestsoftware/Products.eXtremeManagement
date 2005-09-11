from Products.Archetypes.public import *
from Products.CMFCore import CMFCorePermissions
from AccessControl import ClassSecurityInfo
from Products.eXtremeManagement.schemata import *
from Products.eXtremeManagement.config import *
import string

testSchema = BaseSchema.copy()
testSchema['id'].widget.visible = {'edit':'hidden', 'view':'invisible'}

schema = testSchema + ProjectMemberSchema 

class ProjectMember(BaseContent):
    """A simple archetype"""
    schema                = schema
    content_icon          = 'user.gif'
    meta_type             = 'Project Member'
    archetype_name        = 'Project Member'
    product_meta_type     = 'Project Member'
    immediate_view        = 'project_member_view'
    default_view          = 'project_member_view'
    allowed_content_types = ([])
    global_allow          = 0
    typeDescription       = ''
    typeDescMsgId         = ''
    security              = ClassSecurityInfo()

    actions = (
               {'id': 'view',
                'name': 'View',
                'action': 'string:${object_url}/project_member_view',
                'permissions': (CMFCorePermissions.View,),
                'category': 'object'},
              )

registerType(ProjectMember, PROJECTNAME)


