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
items = context.portal_catalog.searchResults(portal_type='Task',
                                             path=story_path)
estimate = []
actual = []

if items:
    for item in items:
        obj = item.getObject()
        estimate.append(obj.estimate)
        actual.append(obj.actual)
  
    totalEstimate = sum(estimate)
    totalActual = sum(actual)

    new = float(totalActual)/(totalEstimate)
    progress = round(new*100, 1)

    return progress


else:
    return 0


