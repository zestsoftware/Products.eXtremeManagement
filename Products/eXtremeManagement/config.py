#
# Product configuration. This contents of this module will be imported into
# __init__.py and every content type module.
#
# If you wish to perform custom configuration, you may put a file AppConfig.py
# in your product's root directory. This will be included in this file if
# found.
#
from Products.CMFCore.CMFCorePermissions import setDefaultRoles

PROJECTNAME = "eXtremeManagement"

# Permissions
DEFAULT_ADD_CONTENT_PERMISSION = "Add portal content"
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ('Manager', 'Owner'))
ADD_CONTENT_PERMISSIONS = {
    'ProjectFolder': 'Add ProjectFolder Content',
    'Project': 'Add Project Content',
    'Iteration': 'Add Iteration Content',
    'Story': 'Add Story Content',
    'Task': 'Add Task Content',
    'Booking': 'Add Booking Content',
    'ProjectMember': 'Add ProjectMember Content',
    'Customer': 'Add Customer Content',
    'CustomerFolder': 'Add CustomerFolder Content',
}

setDefaultRoles('Add ProjectFolder Content', ('Manager', 'Owner'))
setDefaultRoles('Add Project Content', ('Manager', 'Owner'))
setDefaultRoles('Add Iteration Content', ('Manager', 'Owner'))
setDefaultRoles('Add Story Content', ('Manager', 'Owner'))
setDefaultRoles('Add Task Content', ('Manager', 'Owner'))
setDefaultRoles('Add Booking Content', ('Manager', 'Owner'))
setDefaultRoles('Add ProjectMember Content', ('Manager', 'Owner'))
setDefaultRoles('Add Customer Content', ('Manager', 'Owner'))
setDefaultRoles('Add CustomerFolder Content', ('Manager', 'Owner'))

product_globals=globals()

##code-section config-bottom #fill in your manual code here
##/code-section config-bottom


# load custom configuration not managed by ArchGenXML
try:
    from Products.eXtremeManagement.AppConfig import *
except ImportError:
    pass

# End of config.py
