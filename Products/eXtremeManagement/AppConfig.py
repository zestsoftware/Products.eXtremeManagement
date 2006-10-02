from Products.CMFCore.utils import getToolByName

STYLESHEETS = [{'id': 'eXtreme.css'}]

DEPENDENCIES = []
GLOBALS = globals()

# For kupu:
OUR_LINKABLE_TYPES = ['Iteration', 'Story']
OUR_COLLECTION_TYPES = ['ProjectFolder', 'Project', 'Iteration']

# For Story.roughEstimate:
HOURS_PER_DAY = 8

# Stories that are not yet completed never reach a progress percentage
# (for the progress bar) of more than this figure.  This way we don't
# get progress percentages of over 100 %.  And we don't give a false
# sense of being almost finished.
MAXIMUM_NOT_COMPLETED_PERCENTAGE = 90

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

NEW_ROLES = ['Employee', 'Customer']


XM_LEFT_SLOTS = ('here/portlet_stories/macros/portlet',)
XM_RIGHT_SLOTS = ('here/portlet_tasks/macros/portlet',
                  'here/portlet_my_projects/macros/portlet',)
