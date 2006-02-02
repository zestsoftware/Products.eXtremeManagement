## Script (Python) "getTasks"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=states=None, showEveryonesTasks=True
##title=Return the number of tasks
##

"""
Parameters:
states: Tasks with these states will be returned.

showEveryonesTasks: if False, only tasks assigned to the current user
will be reported.
"""

# Where do we want to search?
object = context
searchpath = '/'.join(object.getPhysicalPath())

if states is None:
    tasks = context.portal_catalog.searchResults(portal_type='Task',
                                                 path=searchpath)
else:
    tasks = context.portal_catalog.searchResults(portal_type='Task',
                                                 review_state=states,
                                                 path=searchpath)
list = []
if showEveryonesTasks:
    list = tasks
else:
    member = context.portal_membership.getAuthenticatedMember()
    for task in tasks:
        task = task.getObject()
        if task.getAssignees():
            if member.id in task.getAssignees():
                list.append(task)
return list
