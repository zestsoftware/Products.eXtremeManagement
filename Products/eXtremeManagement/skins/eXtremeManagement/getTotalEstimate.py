## Script (Python) "getTotalEstimate"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=obj=None
##title=Get total estimated time
##
if obj:
    current_path = '/'.join(obj.getPhysicalPath())
else:
    current_path = '/'.join(context.getPhysicalPath())

tasks = context.portal_catalog.searchResults(portal_type='Task',
                                             path=current_path)
estimates = []
for task in tasks:
    obj = task.getObject()
    estimates.append(obj.getEstimate())

estimated = sum(estimates)

return str(estimated) + ':00'
