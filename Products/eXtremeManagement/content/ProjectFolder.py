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
    allowed_content_types = ['Project']
    filter_content_types = 1
    global_allow = 1
    content_icon = 'project_icon.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "ProjectFolder"
    typeDescMsgId = 'description_edit_projectfolder'
    _at_rename_after_creation = True
    schema = ProjectFolder_schema

    actions =  ({'action': "string:${object_url}/project_listing",
                 'category': "object",
                 'id': 'view',
                 'name': 'view',
                 'permissions': ("View",),
                 'condition': 'python:1'
                },
                {'id': 'local_roles',
                 'name': 'Sharing',
                 'action': 'string:${object_url}/folder_localrole_form',
                 'permissions': (ManageProperties,)},)

registerType(ProjectFolder, PROJECTNAME)
