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


def strip_uid(attr):
    """
    attr is of the form: 'uid_attribute'.
    split this in 'uid' and 'attribute'.
    """
    if attr.endswith('_hours'):
        return (attr[:-6], 'hours')
    if attr.endswith('_minutes'):
        return (attr[:-8], 'minutes')
    if attr.endswith('_description'):
        return (attr[:-12], 'description')
    return (None, None)


def getValue(attr):
    return REQUEST.form[attr]

for attr in REQUEST.form.keys():
    uid, field = strip_uid(attr)
    if uid and field == 'hours':
        hours = getValue(uid+'_hours')
        minutes = getValue(uid+'_minutes')
        if hours != '0' or minutes != '0':
            brain = context.uid_catalog(UID=uid)
            task = brain[0].getObject()
            booking_date = REQUEST.get('booking_date')
            description = getValue(uid+'_description')
            bookings = task.contentValues()
            idx =1
            while str(idx) in task.objectIds():
                idx = idx + 1

            task.invokeFactory('Booking',
                               idx,
                               title=task.title,
                               description=description,
                               hours=hours,
                               minutes=minutes,
                               bookingDate=booking_date)

return state.set(portal_status_message='Your booking is done!')
