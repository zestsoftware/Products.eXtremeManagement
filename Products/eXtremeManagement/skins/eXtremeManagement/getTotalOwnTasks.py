## Script (Python) "getTotalOwnTasks"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=states=None
##title=Get total estimate, etc for my tasks in the current context
##

"""
Parameters:
states: Tasks with these states will be returned.

"""

required_states = states
# showEveryonesTasks: if False, only tasks assigned to the current user
# will be reported.
showEveryonesTasks = False

# HACK: find a ProjectFolder so we can call the formatTime() function
# from that projectfolder later.
# Batlogg is busy putting that function somewhere else, which is good. :)
pf = context.portal_catalog.searchResults(portal_type='ProjectFolder')
projectFolder = pf[0].getObject()
formatTime = projectFolder.formatTime

def myPortion(task):
    return 1.0/len(task.getAssignees)

tasks = context.getTasks(required_states, showEveryonesTasks)

"""
for task in tasks:
    print 'gre = %r; gra = %r; grd = %s; ass = %r' % (task.getRawEstimate, task.getRawActualHours, task.getRawDifference, task.getAssignees)

"""

rawEstimate = sum([task.getRawEstimate * myPortion(task)
                   for task in tasks])
rawActualHours = sum([task.getRawActualHours * myPortion(task)
                      for task in tasks])
rawDifference = sum([task.getRawDifference * myPortion(task)
                     for task in tasks])
return map(formatTime, (rawEstimate, rawActualHours, rawDifference))
