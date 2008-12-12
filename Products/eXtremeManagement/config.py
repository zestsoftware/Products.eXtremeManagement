from Products.CMFCore.permissions import setDefaultRoles

# One of these could be probably removed
xm_globals = globals()

# Permissions
DEFAULT_ADD_CONTENT_PERMISSION = "Add portal content"
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ('Manager', 'Owner'))
# For xm.tracker
setDefaultRoles("eXtremeManagement: View Tracker",
                ('Projectmanager', 'Employee', 'Manager'))

ADD_CONTENT_PERMISSIONS = {
    'Project': 'eXtremeManagement: Add Project',
    'Iteration': 'eXtremeManagement: Add Iteration',
    'Story': 'eXtremeManagement: Add Story',
    'Task': 'eXtremeManagement: Add Task',
    'PoiTask': 'eXtremeManagement: Add Task',
    'Booking': 'eXtremeManagement: Add Booking',
    'Offer': 'eXtremeManagement: Add Offer',
    # BBB perms below can be removed in release 2.1
    'ProjectMember': 'eXtremeManagement: Add ProjectMember',
    'Customer': 'eXtremeManagement: Add Customer',
    'CustomerFolder': 'eXtremeManagement: Add CustomerFolder',
    'ProjectFolder': 'eXtremeManagement: Add ProjectFolder',
}

# For kupu:
OUR_LINKABLE_TYPES = [
    'Iteration',
    'Offer',
    'PoiTask',
    'Project',
    'Story',
    'Task',
    # BBB types below can be removed in release 2.1
    'CustomerFolder',
    'Customer',
    'ProjectFolder',
    'ProjectMember',
    ]

OUR_COLLECTION_TYPES = [
    'Iteration',
    'Offer',
    'PoiTask',
    'Project',
    'Story',
    # BBB types below can be removed in release 2.1
    'CustomerFolder',
    'Customer',
    'ProjectFolder',
    'ProjectMember',
    ]

NEW_ROLES = ['Employee', 'Customer', 'Projectmanager']
