## Script (Python) "getOpenTasks"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=storyObj
##title=Get open taks
##

unfinished_states = ('open','assigned','in-progress',)

story_path = '/'.join(storyObj.getPhysicalPath())
items = context.portal_catalog.searchResults(portal_type='Task', 
                                             review_state=unfinished_states, 
                                             path=story_path)
list = []
for item in items:
    list.append(item.id)

return len(list)

