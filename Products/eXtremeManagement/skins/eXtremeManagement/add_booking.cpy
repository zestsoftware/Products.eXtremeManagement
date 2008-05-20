## Script (Python) "add_booking"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Update the actual hours on open tasks
##
REQUEST = context.REQUEST


def getValue(attr):
    return REQUEST.form[attr]

for key in REQUEST.form.keys():
    if key == 'hours':
        hours = getValue('hours')
    if key == 'minutes':
        minutes = getValue('minutes')
    if key == 'description':
        description = getValue('description')

if hours != '0' or minutes != '0':
    bookings = context.contentValues()
    idx =1
    while str(idx) in task.objectIds():
        idx = idx + 1

    task.invokeFactory('Booking',
                        idx,
                        title=task.title,
                        description=description,
                        hours=hours,
                        minutes=minutes)

return state.set(portal_status_message='Your booking is done!')
