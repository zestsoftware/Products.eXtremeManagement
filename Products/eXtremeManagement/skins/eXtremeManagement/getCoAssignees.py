## Script (Python) "getCoAssignees"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Return the co-assignees for a task
##

task = context
member = context.portal_membership.getAuthenticatedMember()
member_id = member.id
list = []

if task.getAssignees():
    for id in task.getAssignees():
        if id != member_id:
            list.append(id)

return list
