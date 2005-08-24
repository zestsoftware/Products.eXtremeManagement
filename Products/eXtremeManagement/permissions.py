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

ChangeProjectFolder = "eXtremeManagement: Change Project Folder"
ChangeProject = "eXtremeManagement: Change Project"
ChangeCustomerFolder = "eXtremeManagement: Change Customer Folder"
ChangeCustomer = "eXtremeManagement: Change Customer"
ChangeIteration = "eXtremeManagement: Change Iteration"
ChangeStory = "eXtremeManagement: Change Story"
ChangeTask = "eXtremeManagement: Change Task"
ChangeProjectMember = "eXtremeManagement: Change Project Member"

# Set up default roles for permissions
#setDefaultRoles(AddProjectFolder, AddProject, AddTask, ('Manager','Employee',))
#setDefaultRoles(AddIteration, AddStory, AddProjectMember('Manager', 'Employee', 'Customer'))
#
#setDefaultRoles(ChangeProjectFolder, ChangeProject, ChangeTask, ('Manager', 'Owner'))
#setDefaultRoles(ChangeIteration, ChangeStory, ChangeProjectMember('Manager','Employee', 'Customer')) 


# Default Permissions Role Map
DefaultPermissionRoleMap = {}

RolePermissionMap={'Employee':(AddProjectFolder, AddProject, AddIteration, AddStory, AddTask, AddProjectMember, 
                               AddCustomerFolder, AddCustomer, ChangeProjectFolder, ChangeCustomerFolder, 
                               ChangeCustomer, ChangeProject, ChangeStory, ChangeTask, ChangeProjectMember),
                   'Customer':(AddIteration, AddTask, AddProjectMember, 
                               ChangeIteration, ChangeTask, ChangeProjectMember),
                  } 


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


