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

"""
import logging
log = logging.getLogger("Daily Bookings")
"""


# Where do we want to search?
searchpath = '/'.join(context.getPhysicalPath())

if memberid is None:
    member = context.portal_membership.getAuthenticatedMember()
    memberid = member.id

if date is None:
    date = DateTime()

# HACK: find a ProjectFolder so we can call the formatTime() function
# from that projectfolder later.
# Batlogg is busy putting that function somewhere else, which is good. :)
pf = context.portal_catalog.searchResults(portal_type='ProjectFolder')
projectFolder = pf[0].getObject()
formatTime = projectFolder.formatTime

startDate = DateTime.earliestTime(date)
endDate = DateTime.latestTime(date)

bookingbrains = context.portal_catalog.searchResults(
    portal_type='Booking',
    getBookingDate={ "query": [startDate, endDate], "range": "minmax"},
    Creator=memberid,
    path=searchpath)

total = 0
if bookingbrains:
    actualList = []
    for bb in bookingbrains:
        actualList.append(bb.getRawActualHours)
    total = sum(actualList)
    total = formatTime(total)

return total
