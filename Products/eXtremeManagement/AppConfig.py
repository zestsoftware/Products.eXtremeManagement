STYLESHEETS = [{'id': 'eXtreme.css'}]

DEPENDENCIES = ['Poi','AddRemoveWidget','DataGridField','kupu']
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
