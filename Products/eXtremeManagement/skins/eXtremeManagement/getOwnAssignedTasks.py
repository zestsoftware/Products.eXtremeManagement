## Script (Python) "getOwnAssignedTasks"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Get own tasks that have state 'assigned' in the current context
##

required_states = ('assigned',)
showEveryonesTasks = False
return context.getTasks(required_states, showEveryonesTasks)
