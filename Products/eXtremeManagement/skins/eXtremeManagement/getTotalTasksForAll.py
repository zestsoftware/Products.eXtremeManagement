## Script (Python) "getTotalOwnTasks"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=states=None
##title=Get a list for each user of total estimate, etc for tasks in
##the current context
##

"""
Parameters:
states: Tasks with these states will be returned.

"""

xt = context.xm_tool

# Where do we want to search?
searchpath = '/'.join(context.getPhysicalPath())

if states is None:
    taskbrains = context.portal_catalog.searchResults(portal_type='Task',
                                                 path=searchpath)
else:
    taskbrains = context.portal_catalog.searchResults(portal_type='Task',
                                                 review_state=states,
                                                 path=searchpath)

def myPortion(task):
    return 1.0/len(task.getAssignees)

list = []
members = context.getProject().getMembers()
for memberid in members:
    tasks = [taskbrain for taskbrain in taskbrains
                    if memberid in taskbrain.getAssignees]
    rawEstimate = sum([task.getRawEstimate * myPortion(task)
                       for task in tasks])
    if rawEstimate > 0:
        # We should get bookings here.
        bookings = context.portal_catalog.searchResults(
            portal_type='Booking',
            Creator=memberid,
            path=searchpath)
        #rawActualHours = sum([task.getRawActualHours * myPortion(task)
        #                      for task in tasks])
        #rawDifference = sum([task.getRawDifference * myPortion(task)
        #                     for task in tasks])
        rawActualHours = sum([booking.getRawActualHours for booking in bookings])
        rawDifference = rawEstimate - rawActualHours
        list.append((memberid,
                     map(xt.formatTime, (rawEstimate, rawActualHours, rawDifference))))

return list
