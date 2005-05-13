## Script (Python) "getTotalEstimate"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Get total estimated time
##

items = context.contentValues('Task')
list = []
for item in items:
    list.append(item.estimate)

newlist = sum(list)

return newlist

