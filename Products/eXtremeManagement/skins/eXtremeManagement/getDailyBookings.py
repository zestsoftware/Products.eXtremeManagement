## Script (Python) "getDailyBookings"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Return the daily Bookings for some period of a person
##

"""
This function returns a list of tuples (date, totallyBooked).

If totallyBooked is 0, nothing is returned for that date.


REQUEST Parameters:
memberid: member id to get this booking list of.
  Standard: None, which means, just the current logged in member.

year: year to display

month: month to display

previous: use previous month instead

next: use next month instead

I don't yet now a sane way to use year and month from a template.
Stick to previous for the moment then.

"""

def getNextYearMonth(year, month):
    # Get the year and month for next month (watch out for December)
    nextyear = year + month/12
    nextmonth = (month % 12) + 1
    return (nextyear, nextmonth)

def getPrevYearMonth(year, month):
    # Get the year and month for the previous month (watch out for January)
    prevmonth = month - 1
    prevyear = year
    if prevmonth == 0:
        prevyear = year - 1
        prevmonth = 12
    return (prevyear, prevmonth)

REQUEST=context.REQUEST

year = None
month = None
previous = None
next = None
memberid = None
for attr in REQUEST.form.keys():
    try:
        value = int(REQUEST.form[attr])
    except:
        value = None
    if attr == 'previous':
        previous = value
    elif attr == 'next':
        next = value
    elif attr == 'year':
        year = value
    elif attr == 'month':
        month = value
    elif attr == 'memberid':
        memberid = value
    else:
        return None

if year is None:
    year = DateTime().year()

if month is None:
    month = DateTime().month()

if year < 1970:
    return None
if month < 0 or month > 12:
    return None

if previous:
    year, month = getPrevYearMonth(year, month)
if next:
    year, month = getNextYearMonth(year, month)



startDate = DateTime(year, month, 1)
nextyear, nextmonth = getNextYearMonth(year, month)
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

"""
HACK:
>>> from DateTime import DateTime
>>> today=DateTime('2006-02-02')
>>> today
DateTime('2006/02/02')
>>> today+0.99999
DateTime('2006/02/02 23:59:59.136 GMT+0')
"""

while date < endDate:
    bookingbrains = context.portal_catalog.searchResults(portal_type='Booking',
                                                         getBookingDate={ "query": [date, date+0.99999], "range": "minmax"},
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
