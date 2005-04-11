from Products.Archetypes.public import *
from Products.CMFCore import CMFCorePermissions
from AccessControl import ClassSecurityInfo
from Products.eXtremeManagement.schemata import *
from Products.eXtremeManagement.config import *

schema = BaseSchema + CustomerSchema 

class Customer(BaseFolder):
    """A simple folderish archetype"""
    schema                = schema
    content_icon          = 'folder_icon.gif'
    meta_type             = 'Customer'
    archetype_name        = 'Customer'
    product_meta_type     = 'Customer'
    immediate_view        = 'base_view'
    default_view          = 'base_view'
    allowed_content_types = (['ProjectMember',])
    global_allow          = 0
    typeDescription       = ''
    typeDescMsgId         = ''
    security              = ClassSecurityInfo()

    actions = (
               {
                'id': 'view',
                'name': 'View',
                'action': 'string:${object_url}/base_view',
                'permissions': (CMFCorePermissions.View,),
                'category': 'object'
               },
              )

registerType(Customer, PROJECTNAME)


