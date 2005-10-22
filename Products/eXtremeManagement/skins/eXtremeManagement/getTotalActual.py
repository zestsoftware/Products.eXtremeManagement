## Script (Python) "getTotalActual"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=obj=None
##title=Get total actual time
##

if obj:
    current_path = '/'.join(obj.getPhysicalPath())
else:
    current_path = '/'.join(context.getPhysicalPath())

items = context.portal_catalog.searchResults(portal_type='Task',
                                             path=current_path)
time = 0.0
hours = 0
minutes = 0

if items:
    for item in items:
        obj = item.getObject()
        time = time + obj.get_actual_hours()

    hours = int(time)
    minutes = int((time - hours)*60)
    if minutes == 0:
        minutes = '00'
    return ('%s:%s' % (hours, minutes))
else:
    return '0:00'

