## Script (Python) "getFilteredTasks"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=filters={},createdByMe=False,assignedToMe=False,onlyTodo=False
##title=getFilteredTasks
##

## returns all tasks (eXtremeManagement) defined in the path
## of ``context`` and match the given filter.
## filter is a dictionary containing portal_catalog queries


from Products.CMFCore.utils import getToolByName

pc = getToolByName(context, 'portal_catalog')


searchFilter = filters
searchFilter['portal_type'] = 'Task'
searchFilter['path'] = '/'.join(context.getPhysicalPath())

if assignedToMe:
    mtool = getToolByName(context, 'portal_membership')
    currentUser = mtool.getAuthenticatedMember().getId()
    searchFilter['getAssignees'] = currentUser


if createdByMe:
    mtool = getToolByName(context, 'portal_membership')
    currentUser = mtool.getAuthenticatedMember().getId()
    searchFilter['Creator'] = currentUser    

if onlyTodo:
    # we consider the following workflowstates of xm tasks
    # as todo states:
    todoStates = ['open', 'to-do']
    searchFilter['review_state'] = todoStates
    
return pc(searchFilter)
