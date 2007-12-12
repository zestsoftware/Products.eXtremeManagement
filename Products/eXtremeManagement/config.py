from Products.CMFCore.permissions import setDefaultRoles

# One of these could be probably removed
xm_globals = globals()

# Permissions
DEFAULT_ADD_CONTENT_PERMISSION = "Add portal content"
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ('Manager', 'Owner'))
ADD_CONTENT_PERMISSIONS = {
    'Project': 'eXtremeManagement: Add Project',
    'Iteration': 'eXtremeManagement: Add Iteration',
    'Story': 'eXtremeManagement: Add Story',
    'Task': 'eXtremeManagement: Add Task',
    'PoiTask': 'eXtremeManagement: Add Task',
    'ProjectMember': 'eXtremeManagement: Add ProjectMember',
    'Customer': 'eXtremeManagement: Add Customer',
    'CustomerFolder': 'eXtremeManagement: Add CustomerFolder',
    'ProjectFolder': 'eXtremeManagement: Add ProjectFolder',
    'Booking': 'eXtremeManagement: Add Booking',
}

# For kupu:
OUR_LINKABLE_TYPES = ['Iteration', 'Story']
OUR_COLLECTION_TYPES = ['ProjectFolder', 'Project', 'Iteration']

XM_LEFT_SLOTS = ('here/portlet_stories/macros/portlet',)
XM_RIGHT_SLOTS = ('here/portlet_tasks/macros/portlet',
                  'here/portlet_my_projects/macros/portlet',)

NEW_ROLES = ['Employee', 'Customer', 'Projectmanager']

# Here we can turn graphs on or off
GRAPHS = False
