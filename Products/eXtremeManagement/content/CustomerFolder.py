from zope.interface import implements
from AccessControl import ClassSecurityInfo
from Products.CMFCore.permissions import ManageProperties
from Products.Archetypes.atapi import *

from Products.eXtremeManagement.config import *
from Products.eXtremeManagement.interfaces import IXMCustomerFolder

FolderSchema = OrderedBaseFolderSchema.copy()
FolderSchema['description'].isMetadata = False
FolderSchema['description'].schemata = 'default'
CustomerFolder_schema = FolderSchema


class CustomerFolder(OrderedBaseFolder):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (OrderedBaseFolder.__implements__,)
    implements(IXMCustomerFolder)

    # This name appears in the 'add' box
    archetype_name = 'CustomerFolder'
    portal_type = meta_type = 'CustomerFolder'
    allowed_content_types = ['Customer']
    filter_content_types = 1
    global_allow = 1
    content_icon = 'group_icon.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "CustomerFolder"
    typeDescMsgId = 'description_edit_customerfolder'
    _at_rename_after_creation = True
    schema = CustomerFolder_schema

    actions =  ({'id'          : 'local_roles',
                 'name'        : 'Sharing',
                 'action'      : 'string:${object_url}/folder_localrole_form',
                 'permissions' : (ManageProperties,)},
        )

registerType(CustomerFolder, PROJECTNAME)
