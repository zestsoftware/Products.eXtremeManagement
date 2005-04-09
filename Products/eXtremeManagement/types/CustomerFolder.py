from Products.Archetypes.public import *
from Products.CMFCore import CMFCorePermissions
from AccessControl import ClassSecurityInfo
from Products.eXtremeManagement.schemata import *
from Products.eXtremeManagement.config import *

schema = BaseFolderSchema 

class CustomerFolder(BaseFolder):
    """A simple folderish archetype"""
    schema                = schema
    content_icon          = 'folder_icon.gif'
    meta_type             = 'CustomerFolder'
    archetype_name        = 'CustomerFolder'
    product_meta_type     = 'CustomerFolder'
    immediate_view        = 'folder_listing'
    default_view          = 'folder_listing'
    allowed_content_types = (['Customer',])
    typeDescription       = ''
    typeDescMsgId         = ''
    security              = ClassSecurityInfo()

    actions = (
               {
                'id': 'view',
                'name': 'View',
                'action': 'string:${object_url}/folder_listing',
                'permissions': (CMFCorePermissions.View,),
                'category': 'object'
               },
              )

registerType(CustomerFolder, PROJECTNAME)


