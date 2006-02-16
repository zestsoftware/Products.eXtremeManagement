## Script (Python) "getOwnInProgressTasks"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Get own tasks that are to-do in the current context
##

required_states = ('to-do',)
showEveryonesTasks = False
return context.getTasks(required_states, showEveryonesTasks)
