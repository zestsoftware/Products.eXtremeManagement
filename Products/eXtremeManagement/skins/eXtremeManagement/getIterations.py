## Script (Python) "getIterations"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=states=None
##title=Return the iterations, in catalog form
##

"""
Parameters:
states: Iterations with these states will be returned.
"""

# Where do we want to search?
object = context

brains = object.getFolderContents({'portal_type':'Iteration'})

#states = 'in-progress'
list = []
if states is None:
    list = brains
else:
    for brain in brains:
        if brain.review_state in states:
            list.append(brain)

return list
