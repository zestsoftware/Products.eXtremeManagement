## Script (Python) "update_hours"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Update the actual hours on open tasks
##

REQUEST = context.REQUEST

for uid in REQUEST.form.keys():
    if uid == 'submit':
        continue

    value = REQUEST.form[uid]
    brain = context.uid_catalog(UID=uid)

    try:
        task = brain[0].getObject()

    except IndexError:
        raise "Couldn't find UID %s in the catalog" % uid

    task.setActual(value)
#    print "%s's actual is set to %s" % (task.Title(), task.getActual())

return state.set(portal_status_message='Je uren zijn bijgewerkt!')

