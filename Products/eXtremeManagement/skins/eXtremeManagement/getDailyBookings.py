## Script (Python) "getDailyBookings"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=year=None, month=None, memberid=None
##title=Return the daily Bookings for some period of a person
##

"""
Parameters:
memberid: member id to get this booking list of.
  Standard: None, which means, just the current logged in member.

The period is a month.

This function returns a list of tuples (date, totallyBooked).

If totallyBooked is 0, nothing is returned for that date.
"""

if year is None:
    year = DateTime().year()
if month is None:
    month = DateTime().month()

if year < 1970:
    return None
if month < 0 or month > 12:
    return None

startDate = DateTime(year, month, 1)

# Get the year and month for next month (watch out for December)
nextyear = year + month/12
nextmonth = (month % 12) + 1
endDate = DateTime(nextyear, nextmonth, 1)

# Where do we want to search?
object = context
searchpath = '/'.join(object.getPhysicalPath())

if memberid is None:
    member = context.portal_membership.getAuthenticatedMember()
    memberid = member.id


list = []
date = startDate

# HACK: find a ProjectFolder so we can call the formatTime() function
# from that projectfolder later.
pf = context.portal_catalog.searchResults(portal_type='ProjectFolder')
projectFolder = pf[0].getObject()

while date < endDate:
    bookingbrains = context.portal_catalog.searchResults(portal_type='Booking',
                                                         getBookingDate={ "query": [date, date+1], "range": "minmax"},
                                                         Creator=memberid,
                                                         path=searchpath)

    if bookingbrains:
        actualList = []
        for bb in bookingbrains:
            booking = bb.getObject()
            actualList.append(booking.getRawActualHours())
        total = sum(actualList)
        total = projectFolder.formatTime(total)
        list.append((date, total))
    date += 1

return list
