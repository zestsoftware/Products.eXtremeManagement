## Script (Python) ""
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=states=('open', 'to-do',)
##title=Return the projects that I have tasks in.
##

"""
Parameters:

states: Only projects with tasks for me with these states will be
returned.  Standard: open and to-do, not completed.

"""

# Where do we want to search?
searchpath = '/'.join(context.getPhysicalPath())

projectbrains = context.portal_catalog.searchResults(portal_type='Project',
                                                     path=searchpath)

member = context.portal_membership.getAuthenticatedMember()
memberid = member.id
list = []
for projectbrain in projectbrains:
    searchpath = '/'.join(context.REQUEST.physicalPathFromURL(projectbrain.getURL()))
    if states is None:
        taskbrains = context.portal_catalog.searchResults(portal_type='Task',
                                                          path=searchpath)
    else:
        taskbrains = context.portal_catalog.searchResults(portal_type='Task',
                                                          review_state=states,
                                                          path=searchpath)
    
    # Search for the first assigned Task with member as assignee.
    for taskbrain in taskbrains:
        if memberid in taskbrain.getAssignees:
            list.append(projectbrain)
            break

return list
