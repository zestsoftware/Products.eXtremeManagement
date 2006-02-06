## Script (Python) "getOwnInProgressTasks"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Get own tasks that are in-progress in the current context
##

required_states = ('in-progress',)
showEveryonesTasks = False
return context.getTasks(required_states, showEveryonesTasks)
