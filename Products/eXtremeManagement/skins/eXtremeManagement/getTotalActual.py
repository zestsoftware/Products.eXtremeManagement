## Script (Python) "getTotalActual"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Get total actual time
##

items = context.contentValues('Task')
list = []
for item in items:
    list.append(item.actual)

newlist = sum(list)

return newlist

