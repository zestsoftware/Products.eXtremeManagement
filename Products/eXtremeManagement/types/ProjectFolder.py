from Products.Archetypes.public import *
from Products.CMFCore import CMFCorePermissions
from AccessControl import ClassSecurityInfo
from Products.eXtremeManagement.schemata import *
from Products.eXtremeManagement.config import *
from Products.eXtremeManagement.schemata import DescriptionSchema
import string

schema = DescriptionSchema

class ProjectFolder(OrderedBaseFolder):
    """A simple folderish archetype"""
    schema                = schema
    content_icon          = 'project_icon.gif'
    meta_type             = 'Project Folder'
    archetype_name        = 'Project Folder'
    product_meta_type     = 'Project Folder'
    immediate_view        = 'folder_listing'
    default_view          = 'folder_listing'
    allowed_content_types = (['Project',])
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

registerType(ProjectFolder, PROJECTNAME)


