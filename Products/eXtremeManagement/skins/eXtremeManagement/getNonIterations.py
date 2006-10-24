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

iteration_brains = context.getFolderContents({'portal_type':'Iteration'})
iteration_ids = [brain.id for brain in iteration_brains]
all_brains = context.getFolderContents()
brains = [brain for brain in all_brains
          if brain.id not in iteration_ids]

#states = 'in-progress'
list = []
if states is None:
    list = brains
else:
    for brain in brains:
        if brain.review_state in states:
            list.append(brain)

return list
