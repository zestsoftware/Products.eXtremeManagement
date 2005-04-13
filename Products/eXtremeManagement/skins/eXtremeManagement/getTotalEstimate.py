items = context.contentValues('Task')
list = []
for item in items:
    list.append(item.estimate)

newlist = sum(list)

return newlist

