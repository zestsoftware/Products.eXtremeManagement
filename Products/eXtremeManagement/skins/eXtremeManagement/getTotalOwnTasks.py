## Script (Python) "getTotalOwnTasks"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=states=None
##title=Get total estimate, etc for my tasks in the current context
##

"""
Parameters:
states: Tasks with these states will be returned.

"""

required_states = states
# showEveryonesTasks: if False, only tasks assigned to the current user
# will be reported.
showEveryonesTasks = False

xt = context.xm_tool

def myPortion(task):
    return 1.0/len(task.getAssignees)

tasks = context.getTasks(required_states, showEveryonesTasks)

rawEstimate = sum([task.getRawEstimate * myPortion(task)
                   for task in tasks])
rawActualHours = sum([task.getRawActualHours * myPortion(task)
                      for task in tasks])
rawDifference = sum([task.getRawDifference * myPortion(task)
                     for task in tasks])
return map(xt.formatTime, (rawEstimate, rawActualHours, rawDifference))
