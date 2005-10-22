## Script (Python) "getTotalDifference"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=obj=None
##title=Get total difference between actual and estimate
##

if obj:
    current_path = '/'.join(obj.getPhysicalPath())
else:
    current_path = '/'.join(context.getPhysicalPath())

tasks = context.portal_catalog.searchResults(portal_type='Task',
                                             path=current_path)
estimated = 0.0
actual = 0.0

for task in tasks:
    obj = task.getObject()
    estimated = estimated + float(obj.getEstimate())
    actual = actual + obj.get_actual_hours()

diff = estimated - actual
hours = int(diff)        
minutes = int((diff - hours)*60)

if minutes == 0:
    minutes = '00'
if minutes < 0:
    minutes = minutes*-1

return ('%s:%s' % (hours, minutes))
