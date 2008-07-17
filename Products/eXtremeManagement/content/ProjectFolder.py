from zope.interface import implements
from AccessControl import ClassSecurityInfo

from Products.Archetypes.atapi import OrderedBaseFolder
from Products.Archetypes.atapi import OrderedBaseFolderSchema
from Products.Archetypes.atapi import registerType

from Products.eXtremeManagement.interfaces import IXMProjectFolder

FolderSchema = OrderedBaseFolderSchema.copy()
FolderSchema['description'].isMetadata = False
FolderSchema['description'].schemata = 'default'
ProjectFolder_schema = FolderSchema

# BBB Can be removed in release 2.1

class ProjectFolder(OrderedBaseFolder):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (OrderedBaseFolder.__implements__, )
    implements(IXMProjectFolder)

    # This name appears in the 'add' box
    archetype_name = 'Project Folder'
    portal_type = meta_type = 'ProjectFolder'
    _at_rename_after_creation = True
    schema = ProjectFolder_schema


registerType(ProjectFolder, 'eXtremeManagement')
