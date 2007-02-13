## Script (Python) "getSortedBookings"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Return the bookingDate sorted Bookings
##

current_path = '/'.join(context.getPhysicalPath())

bookings = [brain.getObject() for brain in
            context.portal_catalog.searchResults(portal_type='Booking',
                                              sort_on='getBookingDate',
                                              path=current_path)]

return bookings
