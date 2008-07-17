from zope.interface import implements
from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import OrderedBaseFolderSchema
from Products.Archetypes.atapi import OrderedBaseFolder
from Products.Archetypes.atapi import registerType

from Products.eXtremeManagement.interfaces import IXMCustomerFolder

FolderSchema = OrderedBaseFolderSchema.copy()
FolderSchema['description'].isMetadata = False
FolderSchema['description'].schemata = 'default'
CustomerFolder_schema = FolderSchema

# BBB Can be removed in release 2.1

class CustomerFolder(OrderedBaseFolder):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (OrderedBaseFolder.__implements__, )
    implements(IXMCustomerFolder)

    # This name appears in the 'add' box
    archetype_name = 'CustomerFolder'
    portal_type = meta_type = 'CustomerFolder'
    typeDescription = "CustomerFolder"
    typeDescMsgId = 'description_edit_customerfolder'
    _at_rename_after_creation = True
    schema = CustomerFolder_schema


registerType(CustomerFolder, 'eXtremeManagement')
