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
        # Should not be needed, but let's add this anyway
        if self.request.get('form') is None:
            self.request.form = {}

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
        nextyear, nextmonth = getNextYearMonth(self.year, self.month)
        self.endDate = DateTime.latestTime(DateTime(nextyear, nextmonth, 1))

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
