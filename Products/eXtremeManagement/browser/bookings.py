from Products.CMFCore.utils import getToolByName
from DateTime import DateTime
from Products.Five.browser import BrowserView
from Acquisition import aq_inner
from Products.eXtremeManagement.browser.xmbase import XMBaseView
from xm.booking.timing.interfaces import IActualHours
from Products.eXtremeManagement.utils import formatTime


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


class BookingsDetailedView(BrowserView):
    """Return a list of Bookings.
    """
    request = None
    context = None
    bookinglist = []

    def __init__(self, context, request, year=None, month=None, memberid=None):
        self.context = context
        self.request = request
        context = aq_inner(context)
        self.catalog = getToolByName(context, 'portal_catalog')

        self.year = year or self.request.form.get('year', DateTime().year())
        self.month = month or self.request.form.get('month', DateTime().month())
        self.previous = self.request.form.get('previous')
        self.next = self.request.form.get('next')
        self.memberid = memberid or self.request.form.get('memberid')
        if self.memberid is None:
            member = context.portal_membership.getAuthenticatedMember()
            self.memberid = member.id

        if self.previous:
            self.year, self.month = getPrevYearMonth(self.year, self.month)
        elif self.next:
            self.year, self.month = getNextYearMonth(self.year, self.month)

        self.startDate = DateTime(self.year, self.month, 1)
        self.endDate = getEndOfMonth(self.year, self.month)
        # Where do we want to search?
        self.searchpath = '/'.join(context.getPhysicalPath())
        self.bookinglist = []
        self.raw_total = 0
        self.update()
        self.total = formatTime(self.raw_total)

    def update(self):
        # Get all bookings brains with the given restrictions of
        # period, memberid, etc
        bookingbrains = self.catalog.searchResults(
            portal_type='Booking',
            getBookingDate={ "query": [self.startDate, self.endDate],
                             "range": "minmax"},
            sort_on='getBookingDate',
            Creator=self.memberid,
            path=self.searchpath)

        for bookingbrain in bookingbrains:
            info = self.bookingbrain2extended_dict(bookingbrain)
            self.bookinglist.append(info)
            self.raw_total += bookingbrain.actual_time

    def main(self):
        """Return a dict of the main stuff of this period.
        """
        month_info = dict(
            month = self.month,
            year = self.year,
            raw_total = self.raw_total,
            total = self.total,
            )
        return month_info

    def bookingbrain2extended_dict(self, bookingbrain):
        """Get a dict with extended info from this booking brain.
        """
        context = aq_inner(self.context)

        """
        booking = bookingbrain.getObject()
        project = booking.getProject()
        # This would wake up all objects between the Booking and the Project...
        # So try it via the catalog instead:
        """

        # Get info about grand grand (grand) parent Project
        # Booking is in Task is in Story.
        # Story can be in Iteration or directly in Project.
        bookingpath =  bookingbrain.getPath().split('/')
        path =  '/'.join(bookingpath[:-3])
        search_filter = dict(portal_type='Project', path=path)
        results = self.catalog(**search_filter)
        if len(results) == 0:
            # Presumably we found an Iteration, so try one level up.
            path =  '/'.join(bookingpath[:-4])
            search_filter = dict(portal_type='Project', path=path)
            results = self.catalog(**search_filter)
        try:
            project_title = results[0].Title
        except:
            # If you see this as project title, then you have probably
            # changed eXtremeManagement in such a way that Bookings
            # can be added in places that this code does not expect.
            project_title = 'Unknown project'

        # Get info about parent Task
        path =  '/'.join(bookingpath[:-1])
        search_filter = dict(portal_type=['Task', 'PoiTask'], path=path)
        taskbrain = self.catalog(**search_filter)[0]

        returnvalue = dict(
            booking_date = context.restrictedTraverse('@@plone').toLocalizedTime(bookingbrain.getBookingDate),
            day_of_week = bookingbrain.getBookingDate.Day(),
            project_title = project_title,
            task_url = taskbrain.getURL(),
            task_title = taskbrain.Title,
            # base_view of a booking gets redirected to the task view,
            # which we do not want here.
            booking_url = bookingbrain.getURL() + '/base_edit',
            booking_title = bookingbrain.Title,
            booking_description = bookingbrain.Description,
            booking_hours = formatTime(bookingbrain.actual_time),
            creator = bookingbrain.Creator,
        )
        return returnvalue


class BookingOverview(BookingsDetailedView):
    """View an overview of Bookings.
    """

    def update(self):
        context = aq_inner(self.context)
        request = self.request
        day = 1
        date = self.startDate
        # We loop until we catch a DateError really, but let's throw
        # in another check so there is even less chance of looping
        # forever.
        while day < 32:
            opts = dict(date=date, memberid=self.memberid)
            days_bookings = DayBookingOverview(context, request, **opts)
            if days_bookings.raw_total > 0:
                self.bookinglist.append((date, days_bookings.total, date.Day()))
                self.raw_total += days_bookings.raw_total
            day += 1
            try:
                # We used to simply do date + 1, but that gave problems with
                # Daylight Savings Time.
                date = DateTime(self.year, self.month, day)
            except DateTime.DateError:
                break


class WeekBookingOverview(BookingsDetailedView):
    """View an overview of Bookings.
    """

    def update(self):
        context = aq_inner(self.context)
        request = self.request
        weeklist = []
        # Start at first day of the week
        # With the DateTime.week() method Monday is considered the first day.
        date = self.startDate - self.startDate.dow() + 1
        # Assemble info for at most one month:
        while date.month() <= self.month and date.year() <= self.year:
            weekinfo = dict(
                week_number = date.week(),
                week_start = context.restrictedTraverse('@@plone').toLocalizedTime(date),
                )
            # Start the week cleanly
            day = 0
            daylist = []
            raw_total = 0.0
            while day < 7:
                opts = dict(date=date, memberid=self.memberid)
                days_bookings = DayBookingOverview(context, request, **opts)
                if days_bookings.raw_total > 0:
                    daylist.append(dict(total=days_bookings.total, day_of_week=date.Day()))
                else:
                    daylist.append(dict(total=None, day_of_week=date.Day()))
                raw_total += days_bookings.raw_total
                day += 1
                date += 1
            # Add the info to the dict for this week
            weekinfo['days'] = daylist
            weekinfo['week_total'] = formatTime(raw_total)
            self.bookinglist.append(weekinfo)
            # update month total
            self.raw_total += raw_total


class YearBookingOverview(BrowserView):
    request = None
    context = None
    months_list = []

    def __init__(self, context, request):
        super(YearBookingOverview, self).__init__(context, request)
        context = aq_inner(context)
        self.catalog = getToolByName(context, 'portal_catalog')

        self.base_year = int(self.request.form.get('base_year', DateTime().year()))
        self.base_month = DateTime().month()
        self.raw_total = 0.0
        self.update()
        self.total = formatTime(self.raw_total)

    def main(self):
        """Return a dict of the main stuff of this period.
        """
        returnvalue = dict(
            base_year = self.base_year,
            base_month = self.base_month,
            prev_year = self.base_year - 1,
            next_year = self.base_year + 1,
            display_next_year = self.base_year < DateTime().year(),
            total = self.total,
            )
        return returnvalue

    def update(self):
        context = aq_inner(self.context)
        request = self.request
        self.months_list = []
        month = self.base_month
        year = self.base_year
        
        for dmonth in range(12):
            year, month = getPrevYearMonth(year, month)
            opts = dict(year=year, month=month)
            bookview = WeekBookingOverview(context, request, **opts)
            main = bookview.main()
            month_info = dict(
                main = main,
                bookings = bookview.bookinglist,
                )
            self.months_list.append(month_info)
            self.raw_total += main['raw_total']


class BookingView(XMBaseView):
    """Simply return info about a Booking.
    """
 
    def main(self):
        """Get a dict with info from this Booking.
        """
        context = aq_inner(self.context)
        workflow = getToolByName(context, 'portal_workflow')
        anno = IActualHours(context, None)
        if anno is not None:
            actual = anno.actual_time
        else:
            # What the???
            actual = -99.0
        returnvalue = dict(
            title = context.title_or_id(),
            description = context.Description(),
            actual = formatTime(actual),
            booking_date = context.restrictedTraverse('@@plone').toLocalizedTime(context.getBookingDate()),
            billable = context.getBillable(),
            creator = context.Creator(),
            # base_view of a booking gets redirected to the task view,
            # which we do not want here.
            url = context.absolute_url() + '/base_edit',
            )
        return returnvalue


class DayBookingOverview(BrowserView):
    request = None
    context = None
    raw_total = 0.0
    total = '0:00'

    def __init__(self, context, request, memberid=None, date=None):
        super(DayBookingOverview, self).__init__(context, request)
        context = aq_inner(context)
        self.catalog = getToolByName(context, 'portal_catalog')

        self.memberid = memberid or self.request.form.get('memberid')
        if self.memberid is None:
            member = context.portal_membership.getAuthenticatedMember()
            self.memberid = member.id
        # Where do we want to search?
        self.searchpath = '/'.join(context.getPhysicalPath())

        self.date = date or self.request.form.get('date', DateTime().earliestTime())
        self.update()
        
    def update(self):
        bookingbrains = self.catalog.searchResults(
            portal_type='Booking',
            getBookingDate=self.date,
            Creator=self.memberid,
            path=self.searchpath)

        if bookingbrains:
            actualList = []
            for bb in bookingbrains:
                actualList.append(bb.actual_time)
            self.raw_total = sum(actualList)
        self.total = formatTime(self.raw_total)
