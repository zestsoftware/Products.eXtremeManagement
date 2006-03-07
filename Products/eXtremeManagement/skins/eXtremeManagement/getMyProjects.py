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
object = context
searchpath = '/'.join(object.getPhysicalPath())

projectbrains = context.portal_catalog.searchResults(portal_type='Project',
                                                     path=searchpath)

member = context.portal_membership.getAuthenticatedMember()
list = []
for projectbrain in projectbrains:
    project = projectbrain.getObject()
    searchpath = '/'.join(project.getPhysicalPath())
    if states is None:
        taskbrains = context.portal_catalog.searchResults(portal_type='Task',
                                                          path=searchpath)
    else:
        taskbrains = context.portal_catalog.searchResults(portal_type='Task',
                                                          review_state=states,
                                                          path=searchpath)
    
    # Search for the first assigned Task with member as assignee.
    for taskbrain in taskbrains:
        task = taskbrain.getObject()
        if task.getAssignees():
            if member.id in task.getAssignees():
                list.append(project)
                break

return list
