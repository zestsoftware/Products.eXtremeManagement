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
AddIteration = "eXtremeManagement: Add Iteration"
AddStory = "eXtremeManagement: Add Story"
AddTask = "eXtremeManagement: Add Task"

ChangeProjectFolder = "eXtremeManagement: Change Project Folder"
ChangeProject = "eXtremeManagement: Change Project"
ChangeIteration = "eXtremeManagement: Change Iteration"
ChangeStory = "eXtremeManagement: Change Story"
ChangeTask = "eXtremeManagement: Change Task"

# Set up default roles for permissions
setDefaultRoles(AddProjectFolder, AddProject, AddTask, ('Manager','Employee',))
setDefaultRoles(AddIteration, AddStory, ('Manager', 'Employee', 'Customer'))

setDefaultRoles(ChangeProjectFolder, ChangeProject, ChangeTask, ('Manager', 'Owner',))
setDefaultRoles(ChangeIteration, ChangeStory, ('Manager','Employee', 'Customer')) 



#################################
# Default Permissions Role Map
DefaultPermissionRoleMap = {}


#################################
# used by initialization to map content types to permissions

ContentPermissionMap = ContentPermMap()
ContentPermissionMap[ AddProjectFolder ] = 'ProjectFolder'
ContentPermissionMap[ AddProject ]       = 'Project'
ContentPermissionMap[ AddIteration ]     = 'Iteration'
ContentPermissionMap[ AddStory ]         = 'Story'
ContentPermissionMap[ AddTask ]          = 'Task'
ContentPermissionMap[ CMFPerms.AddPortalContent ] =  None  # our way of saying all else


