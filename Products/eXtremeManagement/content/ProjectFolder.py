from zope.interface import implements
from AccessControl import ClassSecurityInfo

from Products.CMFCore.permissions import ManageProperties
from Products.Archetypes.atapi import *

from Products.eXtremeManagement.config import *
from Products.eXtremeManagement.interfaces import IXMProjectFolder

FolderSchema = OrderedBaseFolderSchema.copy()
FolderSchema['description'].isMetadata = False
FolderSchema['description'].schemata = 'default'
ProjectFolder_schema = FolderSchema


class ProjectFolder(OrderedBaseFolder):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (OrderedBaseFolder.__implements__,)
    implements(IXMProjectFolder)

    # This name appears in the 'add' box
    archetype_name = 'Project Folder'
    portal_type = meta_type = 'ProjectFolder'
    _at_rename_after_creation = True
    schema = ProjectFolder_schema


registerType(ProjectFolder, PROJECTNAME)
