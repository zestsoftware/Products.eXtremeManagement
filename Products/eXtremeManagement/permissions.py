"""
$Id: $
"""
from AccessControl import Permissions as ZPerms
from Products.CMFCore import CMFCorePermissions as CMFPerms
from Products.GroupUserFolder import GroupsToolPermissions as GRUFPerms
#from Products.CMFMember import MemberPermissions as MemberPerms
#from utils import ContentPermMap

# Roles
eXtremeManagementRoles = ['Employee', 'Customer',]


# Role -> Permission Mapping

#RolePermissionMap = {
#                     'Employee':( CMFPerms.ManageProperties, CMFPerms.DeleteObjects, GRUFPerms.ViewGroups, CMFPerms.SetOwnProperties,
#                                  CMFPerms.AddPortalContent, CMFPerms.View, CMFPerms.ModifyPortalContent, CMFPerms.ListFolderContents ),
#                     'Customer':( CMFPerms.View, ),
#                    }

#################################
# Default Permissions Role Map
DefaultPermissionRoleMap = {}


