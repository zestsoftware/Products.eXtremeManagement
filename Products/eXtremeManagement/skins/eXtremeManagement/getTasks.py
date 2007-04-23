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

filter = dict(portal_type='Task',
              review_state=states,
              path=searchpath)

if not showEveryonesTasks:
    member = context.portal_membership.getAuthenticatedMember()
    filter['getAssignees'] = member.id

return context.portal_catalog.searchResults(**filter)
