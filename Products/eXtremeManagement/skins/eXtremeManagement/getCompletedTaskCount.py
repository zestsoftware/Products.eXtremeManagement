## Script (Python) "getCompletedTaskCount"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Get completed tasks
##

finished_states = ('completed',)
showEveryonesTasks = True
return len(context.getTasks(finished_states, showEveryonesTasks))
