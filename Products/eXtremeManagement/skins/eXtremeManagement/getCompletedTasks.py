## Script (Python) "getCompletedTasks"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=storyObj
##title=Get completed tasks
##

story_path = '/'.join(storyObj.getPhysicalPath())
items = context.portal_catalog.searchResults(portal_type="Task", 
                                             review_state="completed", 
                                             path=story_path)
list = []
for item in items:
    list.append(item.id)

return len(list)

