from Products.CMFCore.utils import getToolByName
from DateTime import DateTime


def getNextYearMonth(year, month):
    """Get the year and month for next month (watch out for December)

    >>> getNextYearMonth(2007, 1)
    (2007, 2)
    >>> getNextYearMonth(2006, 12)
    (2007, 1)

    What happens when we use a wrong month number?

    >>> getNextYearMonth(2007, 13)
    Traceback (most recent call last):
    ...
    ValueError
    >>> getNextYearMonth(2007, 0)
    Traceback (most recent call last):
    ...
    ValueError

    """
    if month < 1 or month > 12:
        raise ValueError
    nextyear = year + month/12
    nextmonth = (month % 12) + 1
    return (nextyear, nextmonth)


def getPrevYearMonth(year, month):
    """Get the year and month for the previous month (watch out for January)

    >>> getPrevYearMonth(2007, 2)
    (2007, 1)
    >>> getPrevYearMonth(2007, 1)
    (2006, 12)

    What happens when we use a wrong month number?

    >>> getPrevYearMonth(2007, 13)
    Traceback (most recent call last):
    ...
    ValueError
    >>> getPrevYearMonth(2007, 0)
    Traceback (most recent call last):
    ...
    ValueError

    Now test this in combination with getNextYearMonth.  These two
    functions should be the reverse of each other.  So this should
    return nothing.  (Note: month range 1 to 13 excludes 13.)

    >>> for month in range(1,13):
    ...     y, m = getNextYearMonth(2007, month)
    ...     if not getPrevYearMonth(y, m) == (2007, month):
    ...         print month
    ...     y, m = getPrevYearMonth(2007, month)
    ...     if not getNextYearMonth(y, m) == (2007, month):
    ...         print month


    """
    if month < 1 or month > 12:
        raise ValueError
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
        self.xt = getToolByName(self.context, 'xm_tool')
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

        for bookingbrain in bookings:
            info = self.bookingInfo(bookingbrain)
            list.append(info)

        return list

    def bookingInfo(self, bookingbrain):
        """Get a dict with info from this booking brain.
        To do: get rid of the getObject call.
        """
        booking_date = self.context.toLocalizedTime(bookingbrain.getBookingDate, long_format=0)
        booking = bookingbrain.getObject()
        project_title = booking.getProject().Title()
        task = booking.aq_parent
        task_url = task.absolute_url()
        task_title = task.Title()
        booking_url = booking.absolute_url()
        booking_title = bookingbrain.Title
        booking_description = bookingbrain.Description
        booking_hours = self.xt.formatTime(bookingbrain.getRawActualHours)
        returnvalue = {
            'booking_date': booking_date,
            'project_title': project_title,
            'task_url': task_url,
            'task_title': task_title,
            'booking_url': booking_url,
            'booking_title': booking_title,
            'booking_description': booking_description,
            'booking_hours': booking_hours,
            }
        return returnvalue
