## Script (Python) "getTasks"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=states=None, showEveryonesTasks=True
##title=Return the tasks, in catalog form
##

"""
Parameters:
states: Tasks with these states will be returned.

showEveryonesTasks: if False, only tasks assigned to the current user
will be reported.
"""

# Where do we want to search?
searchpath = '/'.join(context.getPhysicalPath())

if states is None:
    taskbrains = context.portal_catalog.searchResults(portal_type='Task',
                                                 path=searchpath)
else:
    taskbrains = context.portal_catalog.searchResults(portal_type='Task',
                                                 review_state=states,
                                                 path=searchpath)

list = []
if showEveryonesTasks:
    list = taskbrains
else:
    member = context.portal_membership.getAuthenticatedMember()
    memberid = member.id
    list = [taskbrain for taskbrain in taskbrains
            if memberid in taskbrain.getAssignees]
return list
