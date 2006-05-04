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
endDate = DateTime(nextyear, nextmonth, 1) - 0.00001


# Where do we want to search?
object = context
searchpath = '/'.join(object.getPhysicalPath())

if memberid is None:
    member = context.portal_membership.getAuthenticatedMember()
    memberid = member.id


bookings = context.portal_catalog.searchResults(portal_type='Booking',
                                                getBookingDate={ "query": [startDate, endDate], "range": "minmax"},
                                                sort_on='getBookingDate',
                                                Creator=memberid,
                                                path=searchpath)
list = []

for booking in bookings:
    booking = booking.getObject()
    list.append(booking)

return list
