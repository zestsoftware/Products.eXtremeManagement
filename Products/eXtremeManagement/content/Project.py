from zope.interface import implements
from AccessControl import ClassSecurityInfo

from Products.CMFCore.utils import getToolByName
from Products.Archetypes.atapi import BooleanField
from Products.Archetypes.atapi import BooleanWidget
from Products.Archetypes.atapi import DecimalWidget
from Products.Archetypes.atapi import FloatField
from Products.Archetypes.atapi import OrderedBaseFolder
from Products.Archetypes.atapi import OrderedBaseFolderSchema
from Products.Archetypes.atapi import registerType
from Products.Archetypes.atapi import Schema

from Products.eXtremeManagement.interfaces import IXMProject

DefaultSchema = Schema((
    FloatField(
        name='budgetHours',
        write_permission="eXtremeManagement: Edit budgetHours",
        validators=('isDecimal', ),
        widget=DecimalWidget(
            description="Enter the budget of the project in hours.",
            label='Budget (hours)',
            label_msgid='label_budgetHours',
            description_msgid='help_budgetHours',
            i18n_domain='eXtremeManagement'),
    ),
    BooleanField('includeGlobalMembers',
        default = True,
        languageIndependent = True,
        widget = BooleanWidget(
            description="If selected, Members with a global role 'Employee' "
                        " will appear in the assignees list of a Task.",
            description_msgid = "help_include_global_members",
            label = "Include global Employees",
            label_msgid = "label_include_global_members",
            i18n_domain = "eXtremeManagement"),
    ),
    BooleanField(
        name='billableProject',
        default="True",
        widget=BooleanWidget(
            label='Billable',
            label_msgid='eXtremeManagement_label_billable',
            i18n_domain='eXtremeManagement')
    ),
), )


FolderSchema = OrderedBaseFolderSchema.copy()
FolderSchema['description'].isMetadata = False
FolderSchema['description'].schemata = 'default'
Project_schema = FolderSchema + DefaultSchema.copy()


class Project(OrderedBaseFolder):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (OrderedBaseFolder.__implements__, )
    implements(IXMProject)

    # This name appears in the 'add' box
    archetype_name = 'Project'
    portal_type = meta_type = 'Project'
    typeDescription = "Project"
    typeDescMsgId = 'description_edit_project'
    _at_rename_after_creation = True
    schema = Project_schema

    security.declarePublic('getLayout')

    def getLayout(self):
        """This exists to please the discussion form.

        Needed because we do not mix in the DynamicViewFTI class.
        Note: this is also used by e.g. Stories by using acquisition.
        """
        return 'base_view'

    security.declarePublic('getProject')

    def getProject(self):
        """
        returns self - useful while doing acquisition many levels down the tree
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
