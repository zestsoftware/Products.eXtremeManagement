items = context.contentValues('Task')
list = []
for item in items:
    list.append(item.actual)

newlist = sum(list)

return newlist

