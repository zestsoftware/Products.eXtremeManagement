from Products.CMFCore.permissions import setDefaultRoles
from Products.CMFCore.utils import getToolByName

PROJECTNAME = "eXtremeManagement"

# One of these could be probably removed
GLOBALS = globals()
product_globals = globals()

# Check for Plone 2.1
try:
    from Products.CMFPlone.migrations import v2_1
except ImportError:
    HAS_PLONE21 = False
else:
    HAS_PLONE21 = True

# Check for GenericSetup
try:
    from Products.GenericSetup import EXTENSION
    HAS_GENERIC_SETUP = True
except:
    HAS_GENERIC_SETUP = False


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

# Dependend products - not quick-installed - used in testcase
# override in custom configuration
PRODUCT_DEPENDENCIES = []
DEPENDENCIES = ['Poi']

# For kupu:
OUR_LINKABLE_TYPES = ['Iteration', 'Story']
OUR_COLLECTION_TYPES = ['ProjectFolder', 'Project', 'Iteration']

XM_LEFT_SLOTS = ('here/portlet_stories/macros/portlet',)
XM_RIGHT_SLOTS = ('here/portlet_tasks/macros/portlet',
                  'here/portlet_my_projects/macros/portlet',)
