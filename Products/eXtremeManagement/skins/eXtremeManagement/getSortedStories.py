## Script (Python) "getSortedStories"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Get open tasks for assignee
##

iteration_path = '/'.join(context.getPhysicalPath())

items = context.portal_catalog.searchResults(portal_type='Story',
                                             sort_on='review_state',
                                             path=iteration_path)

return items
