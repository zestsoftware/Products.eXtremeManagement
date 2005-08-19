## Script (Python) "getOwnTasks"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Get own tasks for update
##

member = context.portal_membership.getAuthenticatedMember()
tasks = context.portal_catalog.searchResults(portal_type='Task',
                                             review_state=['open', 'in-progress'])
list = []

for task in tasks:
    task = task.getObject()
    if task.getAssignees():
        if member.id in task.getAssignees():
            list.append(task)

return list

