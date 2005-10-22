"""
$Id: $
"""
from AccessControl import Permissions as ZPerms
from Products.CMFCore import CMFCorePermissions as CMFPerms
from Products.GroupUserFolder import GroupsToolPermissions as GRUFPerms
from Products.CMFCore.CMFCorePermissions import setDefaultRoles
from utils import ContentPermMap


# Roles
eXtremeManagementRoles = ['Employee', 'Customer',]

#RolePermissionMap={'Employee':(AddProjectFolder, AddProject, AddIteration, AddStory, AddTask, AddProjectMember, 
#                               AddCustomerFolder, AddCustomer, CMFPerms.DeleteObjects, CMFPerms.SetOwnProperties, 
#                               CMFPerms.ManageProperties, CMFPerms.AddPortalContent, CMFPerms.View, 
#                               CMFPerms.ModifyPortalContent, CMFPerms.ListFolderContents)} 

