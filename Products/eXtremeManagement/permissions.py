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


# Permissions
AddProjectFolder = "eXtremeManagement: Add Project Folder"
AddProject = "eXtremeManagement: Add Project"
AddCustomerFolder = "eXtremeManagement: Add Customer Folder"
AddCustomer = "eXtremeManagement: Add Customer"
AddIteration = "eXtremeManagement: Add Iteration"
AddStory = "eXtremeManagement: Add Story"
AddTask = "eXtremeManagement: Add Task"
AddProjectMember = "eXtremeManagement: Add Project Member"

# Set up default roles for permissions
#setDefaultRoles(AddProjectFolder, AddProject, AddTask, ('Manager','Employee',))
#setDefaultRoles(AddIteration, AddStory, AddProjectMember('Manager', 'Employee', 'Customer'))
#setDefaultRoles(ChangeProjectFolder, ChangeProject, ChangeTask, ('Manager', 'Owner'))
#setDefaultRoles(ChangeIteration, ChangeStory, ChangeProjectMember('Manager','Employee', 'Customer')) 



RolePermissionMap={'Employee':(AddProjectFolder, AddProject, AddIteration, AddStory, AddTask, AddProjectMember, 
                               AddCustomerFolder, AddCustomer, CMFPerms.DeleteObjects, CMFPerms.SetOwnProperties, 
                               CMFPerms.ManageProperties, CMFPerms.AddPortalContent, CMFPerms.View, 
                               CMFPerms.ModifyPortalContent, CMFPerms.ListFolderContents),
                   'Customer':(AddIteration, AddStory, AddProjectMember, 
                               CMFPerms.View, CMFPerms.ListFolderContents),
                  } 

# Default Permissions Role Map
DefaultPermissionRoleMap = {}

#################################
# used by initialization to map content types to permissions

ContentPermissionMap = ContentPermMap()
ContentPermissionMap[AddProjectFolder] = 'ProjectFolder'
ContentPermissionMap[AddProject]       = 'Project'
ContentPermissionMap[AddIteration]     = 'Iteration'
ContentPermissionMap[AddStory]         = 'Story'
ContentPermissionMap[AddTask]          = 'Task'
ContentPermissionMap[AddProjectMember] = 'ProjectMember'
ContentPermissionMap[AddCustomerFolder]= 'CustomerFolder'
ContentPermissionMap[AddCustomer]      = 'Customer' 
ContentPermissionMap[CMFPerms.AddPortalContent ] = None 


