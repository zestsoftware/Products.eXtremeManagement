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

# GRUF and PAS are not 100% compatible, at several places we need to
# know, which of them is currently used
try:
    from Products.PlonePAS.pas import getUsers
except ImportError:
    HAS_PAS = False
else:
    HAS_PAS = True
    del getUsers

try:
    from Products.Poi.content.PoiTracker import PoiTracker
except ImportError:
    HAS_POI = False
else:
    HAS_POI = True

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

setDefaultRoles('eXtremeManagement: Add Project', ('Manager','Owner'))
setDefaultRoles('eXtremeManagement: Add Iteration', ('Manager','Owner'))
setDefaultRoles('eXtremeManagement: Add Story', ('Manager','Owner'))
setDefaultRoles('eXtremeManagement: Add Task', ('Manager','Owner'))
setDefaultRoles('eXtremeManagement: Add ProjectMember', ('Manager','Owner'))
setDefaultRoles('eXtremeManagement: Add Customer', ('Manager','Owner'))
setDefaultRoles('eXtremeManagement: Add CustomerFolder', ('Manager','Owner'))
setDefaultRoles('eXtremeManagement: Add ProjectFolder', ('Manager','Owner'))
setDefaultRoles('eXtremeManagement: Add Booking', ('Manager','Owner'))

# Dependend products - not quick-installed - used in testcase
# override in custom configuration
PRODUCT_DEPENDENCIES = []

JAVASCRIPTS = []

STYLESHEETS = [{'id': 'eXtreme.css'}]

DEPENDENCIES = ['Poi']

# For kupu:
OUR_LINKABLE_TYPES = ['Iteration', 'Story']
OUR_COLLECTION_TYPES = ['ProjectFolder', 'Project', 'Iteration']

# For Story.roughEstimate:
HOURS_PER_DAY = 8

NEW_ROLES = ['Employee', 'Customer']

XM_LEFT_SLOTS = ('here/portlet_stories/macros/portlet',)
XM_RIGHT_SLOTS = ('here/portlet_tasks/macros/portlet',
                  'here/portlet_my_projects/macros/portlet',)

# Stories that are not yet completed never reach a progress percentage
# (for the progress bar) of more than this figure.  This way we don't
# get progress percentages of over 100 %.  And we don't give a false
# sense of being almost finished.
MAXIMUM_NOT_COMPLETED_PERCENTAGE = 90
