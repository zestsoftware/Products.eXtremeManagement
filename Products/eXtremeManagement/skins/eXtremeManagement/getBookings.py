## Script (Python) "getBookings"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=memberid=None
##title=Return the Bookings of a person
##

"""
Parameters:
memberid: member id to get this booking list of.
  Standard: None, which means, just the current logged in member.
"""

# Where do we want to search?
object = context
searchpath = '/'.join(object.getPhysicalPath())

if memberid is None:
    member = context.portal_membership.getAuthenticatedMember()
    memberid = member.id


bookings = context.portal_catalog.searchResults(portal_type='Booking',
                                                sort_on='Date',
                                                path=searchpath)
list = []

for booking in bookings:
    booking = booking.getObject()
    list.append(booking)

return list
