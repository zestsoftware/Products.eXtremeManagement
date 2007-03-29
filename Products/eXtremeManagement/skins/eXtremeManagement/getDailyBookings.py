## Script (Python) "getDailyBookings"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=date=None ,memberid=None
##title=Return the daily Bookings for some period of a person
##

"""
Parameters:

date: date to display
memberid: display hours for this member

"""

# Where do we want to search?
searchpath = '/'.join(context.getPhysicalPath())

if memberid is None:
    member = context.portal_membership.getAuthenticatedMember()
    memberid = member.id

if date is None:
    date = DateTime().earliestTime()

xt = context.xm_tool

bookingbrains = context.portal_catalog.searchResults(
    portal_type='Booking',
    getBookingDate=date,
    Creator=memberid,
    path=searchpath)

total = 0
if bookingbrains:
    actualList = []
    for bb in bookingbrains:
        actualList.append(bb.getRawActualHours)
    total = sum(actualList)
    total = xt.formatTime(total)

return total
