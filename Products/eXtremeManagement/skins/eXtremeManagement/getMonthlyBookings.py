## Script (Python) "getMonthlyBookings"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=year=None, month=None
##title=Return the daily Bookings for one month of a person
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


day = 1
startDate = DateTime(year, month, day)
nextyear, nextmonth = getNextYearMonth(year, month)

# Where do we want to search?
object = context
searchpath = '/'.join(object.getPhysicalPath())

if memberid is None:
    member = context.portal_membership.getAuthenticatedMember()
    memberid = member.id


mylist = []
date = startDate

while True:
    total = context.getDailyBookings(date=date, memberid=memberid)
    if total > 0:
        mylist.append((date, total))
    day += 1
    try:
        # We used to simply do date + 1, but that gave problems with
        # Daylight Savings Time.
        date = DateTime(year, month, day)
    except:
        break

return mylist
