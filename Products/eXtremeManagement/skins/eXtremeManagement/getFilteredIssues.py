## Script (Python) "getFilteredIssues"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=filters={},reportedByMe=False,assignedToMe=False,onlyTodo=False
##title=getFilteredIssues
##

## returns all issues (POI) defined in the path
## of ``context`` and match the given filter.
## filter is a dictionary containing portal_catalog queries, eg:
## * filter = {} -> all issues are returned
## * filter = {'state': ['open','unconfirmed']} -> all open or
## unconfirmed issues are returned


from Products.CMFCore.utils import getToolByName

pc = getToolByName(context, 'portal_catalog')


searchFilter = filters
searchFilter['portal_type'] = 'PoiIssue'
searchFilter['path'] = '/'.join(context.getPhysicalPath())

if assignedToMe:
    mtool = getToolByName(context, 'portal_membership')
    currentUser = mtool.getAuthenticatedMember().getId()
    searchFilter['getResponsibleManager'] = currentUser

if reportedByMe:
    mtool = getToolByName(context, 'portal_membership')
    currentUser = mtool.getAuthenticatedMember().getId()
    searchFilter['Creator'] = currentUser    

if onlyTodo:
    # we consider the following workflowstates of poi-issues
    # as todo states:
    todoStates = ['open', 'in-progress', 'unconfirmed']
    searchFilter['review_state'] = todoStates

return  pc(searchFilter)
