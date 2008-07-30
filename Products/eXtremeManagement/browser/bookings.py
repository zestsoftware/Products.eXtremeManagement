from Products.CMFCore.utils import getToolByName
from DateTime import DateTime
from Products.Five.browser import BrowserView
from Acquisition import aq_inner

from xm.booking.timing.interfaces import IActualHours
from Products.eXtremeManagement.browser.xmbase import XMBaseView
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
        self.catalog = getToolByName(context, 'portal_catalog')
        self.year = year or self.request.form.get('year', DateTime().year())
        self.month = month or self.request.form.get('month',
                                                    DateTime().month())
        if isinstance(self.year, basestring):
            self.year = int(self.year)
        if isinstance(self.month, basestring):
            self.month = int(self.month)
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
        self.perc_billable = 0.0
        self.update()

    def update(self):
        # Get all bookings brains with the given restrictions of
        # period, memberid, etc
        bookingbrains = self.catalog.searchResults(
            portal_type='Booking',
            getBookingDate={"query": [self.startDate, self.endDate],
                            "range": "minmax"},
            sort_on='getBookingDate',
            Creator=self.memberid,
            path=self.searchpath)

        for bookingbrain in bookingbrains:
            info = self.bookingbrain2extended_dict(bookingbrain)
            self.bookinglist.append(info)
            self.raw_total += bookingbrain.actual_time

    @property
    def total(self):
        return formatTime(self.raw_total)

    @property
    def fmt_perc_billable(self):
        return "%0.1f" % self.perc_billable + ' %'

    def main(self):
        """Return a dict of the main stuff of this period.
        """
        month_info = dict(
            month = self.month,
            year = self.year,
            raw_total = self.raw_total,
            total = self.total,
            perc_billable = self.fmt_perc_billable,
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
        bookingpath = bookingbrain.getPath().split('/')
        path = '/'.join(bookingpath[:-3])
        search_filter = dict(portal_type='Project', path=path)
        results = self.catalog(**search_filter)
        if len(results) == 0:
            # Presumably we found an Iteration, so try one level up.
            path = '/'.join(bookingpath[:-4])
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
        path = '/'.join(bookingpath[:-1])
        search_filter = dict(portal_type=['Task', 'PoiTask'], path=path)
        taskbrain = self.catalog(**search_filter)[0]

        toLocalizedTime = context.restrictedTraverse('@@plone').toLocalizedTime
        returnvalue = dict(
            booking_date = toLocalizedTime(bookingbrain.getBookingDate),
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
        days_bookings = DayBookingOverview(context, request,
                                           memberid=self.memberid)
        while day < 32:
            day_total = days_bookings.raw_total(date=date)
            if day_total > 0:
                self.bookinglist.append((date, days_bookings.total(date=date),
                                         date.Day()))
                self.raw_total += day_total
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
        # Start at first day of the week.  Note: with the
        # DateTime.week() method Monday is considered the first day,
        # even though DateTime.dow() says Sunday is day zero.  To make
        # things worse, if say Sunday is 1 October, we want to start
        # with the week of Monday 25 September.

        # Go to the beginning of the week that has the first day of
        # this month.  How many days do we have to subtract for that?
        offset = self.startDate.dow() - 1
        if offset < 0:
            # Only happens for Sunday
            offset += 7

        if offset == 0:
            date = self.startDate
            year, month = self.year, self.month
        else:
            year, month = getPrevYearMonth(
                self.year, self.month)
            last_day = getEndOfMonth(year, month).day()
            date = DateTime(year, month, last_day - offset + 1)
        daynumber = date.day()
        # Assemble info for at most one month:
        ploneview = context.restrictedTraverse('@@plone')
        num_weeks = 0
        in_this_month = True

        # When comparing dates, make sure December of previous year is
        # less than January of this year.
        while date.month() + 12 * date.year() <= self.month + 12 * self.year:
            weekinfo = dict(
                week_number = date.week(),
                week_start = ploneview.toLocalizedTime(date),
                )
            # Start the week cleanly
            day_of_week = 0
            daylist = []
            raw_total = 0.0
            days_bookings = DayBookingOverview(context, request,
            memberid=self.memberid)
            week_billable = 0.0
            worked_days = 0
            while day_of_week < 7:
                day_total = days_bookings.raw_total(date=date)
                day_billable = days_bookings.billable(date=date)
                ui_class = 'greyed'
                if day_total > 0:
                    if date.month() == self.startDate.month():
                        raw_total += day_total
                        if day_billable != 0:
                            week_billable += day_billable
                            worked_days += 1
                        ui_class = 'good'
                    else:
                        ui_class = 'greyed'
                    daylist.append(dict(total=formatTime(day_total),
                                        day_of_week=date.Day(),
                                        style=ui_class))
                else:
                    daylist.append(dict(total=None, day_of_week=date.Day(),
                                        style=ui_class))
                day_of_week += 1
                daynumber += 1
                try:
                    # We used to simply do date + 1, but that gave
                    # problems with Daylight Savings Time.
                    date = DateTime(year, month, daynumber)
                except DateTime.DateError:
                    # End of month reached, so go to the next.
                    daynumber = 1
                    year, month = getNextYearMonth(
                        year, month)
                    try:
                        date = DateTime(year, month, daynumber)
                    except DateTime.DateError:
                        # This Should Not Happen (tm)
                        break

            # Add the info to the dict for this week
            weekinfo['days'] = daylist
            weekinfo['week_total'] = formatTime(raw_total)
            if worked_days > 0:
                week_perc_billable = week_billable / worked_days
                num_weeks += 1
            else:
                week_perc_billable = 0.0
            fmt_perc_billable = "%0.1f" % week_perc_billable + ' %'
            weekinfo['total_style'] = weekinfo['perc_style'] = 'greyed'
            if weekinfo['week_number'] < DateTime().week():
                weekinfo['total_style'] = weekinfo['perc_style'] = 'good'
            if raw_total < 40.0 and \
                weekinfo['week_number'] < DateTime().week():
                weekinfo['total_style'] = 'not-enough'
            if week_perc_billable < 0.5 and \
                weekinfo['week_number'] < DateTime().week():
                weekinfo['perc_style'] = 'not-enough'
            weekinfo['perc_billable'] = fmt_perc_billable
            self.bookinglist.append(weekinfo)
            # update month total
            self.raw_total += raw_total
            # add weekly total
            self.perc_billable += week_perc_billable
        # divide by the number of weeks
        if num_weeks > 0:
            self.perc_billable = self.perc_billable / num_weeks


class YearBookingOverview(BrowserView):
    request = None
    context = None
    months_list = []

    def __init__(self, context, request):
        super(YearBookingOverview, self).__init__(context, request)
        self.catalog = getToolByName(context, 'portal_catalog')

        self.base_year = int(self.request.form.get('base_year',
                                                   DateTime().year()))
        self.base_month = DateTime().month()
        self.raw_total = 0.0
        self.update()

    @property
    def total(self):
        return formatTime(self.raw_total)

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
        ploneview = context.restrictedTraverse('@@plone')
        returnvalue = dict(
            title = context.title_or_id(),
            description = context.Description(),
            actual = formatTime(actual),
            booking_date = ploneview.toLocalizedTime(context.getBookingDate()),
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

    def __init__(self, context, request, memberid=None):
        super(DayBookingOverview, self).__init__(context, request)
        self.catalog = getToolByName(context, 'portal_catalog')

        self.memberid = memberid or self.request.form.get('memberid')
        memberid = memberid or self.request.form.get('memberid')
        if self.memberid is None:
            member = context.portal_membership.getAuthenticatedMember()
            self.memberid = member.id
        self.searchpath = '/'.join(context.getPhysicalPath())

    def billable(self, date=None):
        """return a percentage for billable hours"""
        date = date or self.request.form.get('date', DateTime().earliestTime())
        bookingbrains = self.catalog.searchResults(
            portal_type='Booking',
            getBookingDate={"query": [date.earliestTime(), date.latestTime()],
                            "range": "minmax"},
            Creator=self.memberid,
            path=self.searchpath)
        billable=0.0
        for bb in bookingbrains:
            if bb.getBillable:
                billable += bb.actual_time
        if billable == 0:
            return 0.0
        else:
            return billable/8*100

    def raw_total(self, date=None):
        """Raw total booked hours for a member for this date.
        """
        date = date or self.request.form.get('date', DateTime().earliestTime())
        bookingbrains = self.catalog.searchResults(
            portal_type='Booking',
            getBookingDate={"query": [date.earliestTime(),
                                      date.latestTime()],
                            "range": "minmax"},
            Creator=self.memberid,
            path=self.searchpath)

        actualList = []
        for bb in bookingbrains:
            actualList.append(bb.actual_time)
        return sum(actualList)

    def total(self, date=None):
        return formatTime(self.raw_total(date))
