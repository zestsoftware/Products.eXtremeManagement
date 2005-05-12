from Products.Archetypes.public import *
from Products.CMFCore import CMFCorePermissions
from AccessControl import ClassSecurityInfo
from Products.eXtremeManagement.schemata import *
from Products.eXtremeManagement.config import *

from Products.Archetypes.BaseFolder import BaseFolder
from Products.Archetypes.interfaces.orderedfolder import IOrderedFolder
from Products.Archetypes import OrderedBaseFolder
from Products.Archetypes.OrderedBaseFolder import OrderedBaseFolder

schema = OrderedBaseFolderSchema + DescriptionSchema

class CustomerFolder(OrderedBaseFolder):
    """A simple folderish archetype"""
    schema                = schema
    content_icon          = 'group_icon.gif'
    meta_type             = 'Customer Folder'
    archetype_name        = 'Customer Folder'
    product_meta_type     = 'Customer Folder'
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


