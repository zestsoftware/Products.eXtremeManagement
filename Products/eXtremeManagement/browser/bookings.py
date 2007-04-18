from Products.CMFCore.utils import getToolByName
from DateTime import DateTime
from Products.eXtremeManagement.browser.xmbase import XMBaseView
from Products.Five.browser import BrowserView


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


class BookingListView(BrowserView):
    """Return some Bookings.
    """
    bookinglist = []
    total_actual = 0.0

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.catalog = getToolByName(self.context, 'portal_catalog')
        self.xt = getToolByName(self.context, 'xm_tool')

        self.year = self.request.form.get('year', DateTime().year())
        self.month = self.request.form.get('month', DateTime().month())
        self.previous = self.request.form.get('previous')
        self.next = self.request.form.get('next')
        self.memberid = self.request.form.get('next')
        if self.memberid is None:
            member = context.portal_membership.getAuthenticatedMember()
            self.memberid = member.id

        if self.previous:
            self.year, self.month = getPrevYearMonth(self.year, self.month)
        if self.next:
            self.year, self.month = getNextYearMonth(self.year, self.month)

        self.startDate = DateTime(self.year, self.month, 1)
        self.endDate = getEndOfMonth(self.year, self.month)
        # Where do we want to search?
        self.searchpath = '/'.join(self.context.getPhysicalPath())

        self.total_actual = 0
        self.bookinglist = self._make_bookinglist()
        self.total_actual = self.xt.formatTime(self.total_actual)

    def _make_bookinglist(self):
        """List of Bookings that match the REQUEST.

        This also updates the total for this month.
        """


        bookingbrains = self.catalog.searchResults(
            portal_type='Booking',
            getBookingDate={ "query": [self.startDate, self.endDate],
                             "range": "minmax"},
            sort_on='getBookingDate',
            Creator=self.memberid,
            path=self.searchpath)

        booking_list = []

        for bookingbrain in bookingbrains:
            info = self.bookingbrain2extended_dict(bookingbrain)
            booking_list.append(info)
            self.total_actual += bookingbrain.getRawActualHours

        return booking_list

    def bookingbrain2extended_dict(self, bookingbrain):
        """Get a dict with extended info from this booking brain.
        """
        booking = bookingbrain.getObject()
        task = booking.aq_parent
        returnvalue = dict(
            booking_date = self.context.restrictedTraverse('@@plone').toLocalizedTime(bookingbrain.getBookingDate),
            project_title = booking.getProject().Title(),
            task_url = task.absolute_url(),
            task_title = task.Title(),
            # base_view of a booking gets redirected to the task view,
            # which we do not want here.
            booking_url = bookingbrain.getURL() + '/base_edit',
            booking_title = bookingbrain.Title,
            booking_description = bookingbrain.Description,
            booking_hours = self.xt.formatTime(bookingbrain.getRawActualHours),
            creator = bookingbrain.Creator,
        )
        return returnvalue

    def summary_bookinglist(self):
        """Total of Bookings per day
        """
        day = 1
        mylist = []
        date = self.startDate
        while True:
            total = self.context.getDailyBookings(date=date, memberid=self.memberid)
            if total > 0:
                mylist.append((date, total))
            day += 1
            try:
                # We used to simply do date + 1, but that gave problems with
                # Daylight Savings Time.
                date = DateTime(self.year, self.month, day)
            except:
                break
        return mylist


class YearBookingListView(BrowserView):

    def __init__(self, context, request):
        super(YearBookingListView, self).__init__(context, request)
        self.catalog = getToolByName(context, 'portal_catalog')
        self.xt = getToolByName(context, 'xm_tool')

        self.base_year = int(self.request.form.get('base_year', DateTime().year()))
        self.base_month = DateTime().month()
        self.total_yearly = 0

    def main(self):
        """Return a dict of the main stuff of this period.
        """
        context = self.context
        returnvalue = dict(
            base_year = self.base_year,
            base_month = self.base_month,
            prev_year = self.base_year - 1,
            next_year = self.base_year + 1,
            display_next_year = self.base_year < DateTime().year(),
            total_yearly = self.total_yearly,
            )
        return returnvalue

    def year_list(self):
        """Defined with tales in booking_year.pt:


       
        for month in months:
            total_monthly python: 0;
            month python: base_month-dmonth;
            year python: test(month<1, base_year-1, base_year);
            month python: test(month<1, month+12, month);
            current_path python:'/'.join(context.getPhysicalPath());
            bookings python:context.getMonthlyBookings(year=year, month=month)

            for booking in bookings:
                date python:booking[0];
                time python:booking[1];
                daily_total python: time.split(':');
                total_monthly python: total_monthly+int(daily_total[0])+int(int(daily_total[1])/60)
    
            total_yearly python: total_yearly+total_monthly
        """



class BookingView(XMBaseView):
    """Simply return info about a Booking.
    """
 
    def main(self):
        """Get a dict with info from this Booking.
        """
        workflow = getToolByName(self.context, 'portal_workflow')
        returnvalue = dict(
            title = self.context.title_or_id(),
            description = self.context.Description(),
            actual = self.xt.formatTime(self.context.getRawActualHours()),
            booking_date = self.context.restrictedTraverse('@@plone').toLocalizedTime(self.context.getBookingDate()),
            billable = self.context.getBillable(),
            creator = self.context.Creator(),
            # base_view of a booking gets redirected to the task view,
            # which we do not want here.
            url = self.context.absolute_url() + '/base_edit',
            )
        return returnvalue

