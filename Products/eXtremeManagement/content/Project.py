from zope.interface import implements
from AccessControl import ClassSecurityInfo

from Products.CMFCore.utils import getToolByName
from Products.Archetypes.atapi import *

from Products.eXtremeManagement.config import *
from Products.eXtremeManagement.interfaces import IXMProject

MetaSchema = MetadataSchema((
    BooleanField('includeGlobalMembers',
        default = True,
        languageIndependent = True,
        schemata = 'metadata', # moved to 'default' for folders
        widget = BooleanWidget(
            description="If selected, Members with a global role 'Employee' "
                        " will appear in the assignees list of a Task.",
            description_msgid = "help_include_global_members",
            label = "Include global Employees",
            label_msgid = "label_include_global_members",
            i18n_domain = "eXtremeManagement",
            visible=dict(edit=1, view=0)),)
),)

FolderSchema = OrderedBaseFolderSchema.copy()
FolderSchema['description'].isMetadata = False
FolderSchema['description'].schemata = 'default'
Project_schema = FolderSchema +  MetaSchema
Project_schema.moveField('includeGlobalMembers', pos='top')


class Project(OrderedBaseFolder):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (OrderedBaseFolder.__implements__,)
    implements(IXMProject)

    # This name appears in the 'add' box
    archetype_name = 'Project'
    portal_type = meta_type = 'Project'
    typeDescription = "Project"
    typeDescMsgId = 'description_edit_project'
    _at_rename_after_creation = True
    schema = Project_schema

    security.declarePublic('getProject')
    def getProject(self):
        """
        returns self - useful while doing aquisition many levels down the tree
        """
        return self

    security.declarePublic('getMembers')
    def getMembers(self, role='Employee'):
        """
        get a list of all memberids that have the role ``role``
        on this project.
        """
        portal = getToolByName(self, 'portal_url').getPortalObject()
        grp = getToolByName(self, 'portal_groups')
        pu = getToolByName(self, 'plone_utils')
        memberIds=[]

        def _appendGroupsAndUsers(currentIds, extraIds):
            extraUserids = []
            for id in extraIds:
                groupdataobject = grp.getGroupById(id)
                if groupdataobject:
                    #this is a group, we need it's member ids
                    extraUserids += groupdataobject.getMemberIds()
                else:
                    #this is a member, just append it's id
                    extraUserids.append(id)
            for id in extraUserids:
                if id not in currentIds:
                    currentIds.append(id)
            return currentIds

        # member with local role ``role`` on this project
        usersandgroups = self.users_with_local_role(role)
        memberIds = _appendGroupsAndUsers(memberIds, usersandgroups)
        # members that aquired this role
        aquiredGroupsAndUsers = pu.getInheritedLocalRoles(self)
        for name, roles, type, id in aquiredGroupsAndUsers:
            if role in roles:
                if type=='user':
                    memberIds.append(id)
                elif type=='group':
                    memberIds += grp.getGroupById(id).getMemberIds()

        if self.getIncludeGlobalMembers():
            # members that have this role globally
            globalUsers = []
            roleman = portal.acl_users.portal_role_manager
            for userid, loginname in roleman.listAssignedPrincipals(role):
                globalUsers.append(userid)
            memberIds = _appendGroupsAndUsers(memberIds, globalUsers)

        return memberIds


registerType(Project, 'eXtremeManagement')
