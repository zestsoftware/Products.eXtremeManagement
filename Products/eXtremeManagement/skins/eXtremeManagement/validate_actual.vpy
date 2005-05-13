## Controlled Python Script "validate_hours"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=Validates actual hours
##

request = context.REQUEST

# check is entered-actuals are integers

return state
i
# TODO

actual_error = context.check_int(actual, 0, None)
if id_error:
    state.setError('actual', actual_error, new_status='failure')

if state.getErrors():
    return state.set(status='failure', portal_status_message='Please correct the indicated errors.')
else:
    return state
