## Script (Python) ""
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Get completed/invoiced items first, then rest of ordered folder contents
##

items = context.getFolderContents({'portal_type': ['Story', 'Task']})

firstStates = ['completed', 'invoiced']
firstItems = []
otherItems = []

for item in items:
    if item.review_state in firstStates:
        firstItems.append(item)
    else:
        otherItems.append(item)

return firstItems + otherItems
