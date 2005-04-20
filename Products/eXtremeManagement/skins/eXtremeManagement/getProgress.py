## Script (Python) "getProgress"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=storyObj
##title=Get progress
##

story_path = '/'.join(storyObj.getPhysicalPath())
items = context.portal_catalog.searchResults(portal_type="Task",
                                             path=story_path)

estimate = []
actual = []
for item in items:
    obj = item.getObject()
    estimate.append(obj.estimate)
    actual.append(obj.actual)

totalEstimate = str(sum(estimate)) + '.0'
totalActual = str(sum(actual)) + '.0'

newEstimate = float(totalEstimate)
newActual = float(totalActual)

progress = round( (newActual/newEstimate) * 100, 1)

return progress

