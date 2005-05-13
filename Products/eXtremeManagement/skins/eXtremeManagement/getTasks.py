## Script (Python) "getTasks"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Get open tasks for assignee
##

member = context.portal_membership.getAuthenticatedMember()
items = context.portal_catalog.searchResults(portal_type='Task', 
                                             review_state='open')
list = []
for item in items:
    if item.getAssignees:
        if member.id in item.getAssignees:
            list.append(item)

return list

