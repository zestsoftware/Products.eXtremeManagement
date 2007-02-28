from Products.CMFCore.utils import getToolByName
from DateTime import DateTime


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


def getEndOfMonth(year, month):
    """Get the last second of the last day of this month

    First some normal months.

    >>> getEndOfMonth(2007, 1)
    DateTime('2007/01/31 23:59:59 GMT+1')
    >>> getEndOfMonth(2007, 4)
    DateTime('2007/04/30 23:59:59 GMT+2')

    Of course February needs extra testing.

    >>> getEndOfMonth(2007, 2)
    DateTime('2007/02/28 23:59:59 GMT+1')

    2008 is a leap year.

    >>> getEndOfMonth(2008, 2)
    DateTime('2008/02/29 23:59:59 GMT+1')

    """
    
    if month in (1, 3, 5, 7, 8, 10, 12):
        day = 31
    elif month == 2:
        if DateTime(year, 1, 1).isLeapYear():
            day = 29
        else:
            day = 28
    else:
        day = 30
    return DateTime.latestTime(DateTime(year, month, day))


class BookingView(object):
    """Return some Bookings.
    """

    def __init__(self, context, request=None):
        self.context = context
        self.catalog = getToolByName(self.context, 'portal_catalog')
        if request is None:
            # At least handy for testing.
            self.request = self.context.REQUEST
        else:
            self.request = request

        self.year = self.request.get('year', DateTime().year())
        self.month = self.request.get('month', DateTime().month())
        self.previous = self.request.get('previous')
        self.next = self.request.get('next')
        self.memberid = self.request.get('next')
        if self.memberid is None:
            member = context.portal_membership.getAuthenticatedMember()
            self.memberid = member.id

        if self.previous:
            self.year, self.month = getPrevYearMonth(self.year, self.month)
        if self.next:
            self.year, self.month = getNextYearMonth(self.year, self.month)

        self.startDate = DateTime(self.year, self.month, 1)
        self.endDate = getEndOfMonth(self.year, self.month)

    def bookinglist(self):
        """List of Bookings that match the REQUEST.
        """

        if self.year < 1970:
            return []
        if self.month < 0 or self.month > 12:
            return []

        # Where do we want to search?
        searchpath = '/'.join(self.context.getPhysicalPath())

        bookings = self.catalog.searchResults(
            portal_type='Booking',
            getBookingDate={ "query": [self.startDate, self.endDate],
                             "range": "minmax"},
            sort_on='getBookingDate',
            Creator=self.memberid,
            path=searchpath)

        list = []

        for booking in bookings:
            booking = booking.getObject()
            list.append(booking)

        return list
