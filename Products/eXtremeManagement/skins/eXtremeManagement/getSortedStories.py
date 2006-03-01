## Script (Python) ""
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Get completed items first, then rest of ordered folder contents
##

items = context.getFolderContents()

completed = []
uncompleted = []

for item in items:
    if item.review_state == 'completed':
        completed.append(item)
    else:
        uncompleted.append(item)


return completed + uncompleted
