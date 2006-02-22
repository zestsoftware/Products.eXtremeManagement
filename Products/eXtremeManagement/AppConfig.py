STYLESHEETS = [{'id': 'eXtreme.css'}]

DEPENDENCIES = ['Poi','AddRemoveWidget','DataGridField','kupu']
GLOBALS = globals()

# For kupu:
OUR_LINKABLE_TYPES = ['Iteration', 'Story']
OUR_COLLECTION_TYPES = ['ProjectFolder', 'Project', 'Iteration']

# For Story.roughEstimate:
HOURS_PER_DAY = 8

# List of our cts for adding to the factory:
OUR_FACTORY_TYPES = ['ProjectFolder', 'CustomerFolder', 'Customer',
                     'Project', 'Iteration', 'Story', 'Task', 'Booking']
