## Script (Python) "getOwnOpenTasks"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Get open tasks assigned to you in the current context
##

required_states = ('open',)
showEveryonesTasks = False
return context.getTasks(required_states, showEveryonesTasks)
