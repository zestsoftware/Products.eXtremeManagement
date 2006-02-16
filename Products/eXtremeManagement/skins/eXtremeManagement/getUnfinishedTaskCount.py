## Script (Python) "getUnfinishedTaskCount"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Get unfinished task for everyone.
##

unfinished_states = ('open','to-do',)
showEveryonesTasks = True
return len(context.getTasks(unfinished_states, showEveryonesTasks))
