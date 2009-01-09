from zope.cachedescriptors.property import Lazy
from DateTime import DateTime
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName

from xm.booking.timing.interfaces import IActualHours
from Products.eXtremeManagement.browser.xmbase import XMBaseView
from Products.eXtremeManagement.utils import formatTime
from Products.eXtremeManagement.utils import getNextYearMonth
from Products.eXtremeManagement.utils import getPrevYearMonth
from Products.eXtremeManagement.utils import getEndOfMonth


class BookingsDetailedView(XMBaseView):
    """Return a list of Bookings.
    """
    request = None
    context = None
    bookinglist = []

    def __init__(self, context, request, year=None, month=None, memberid=None):
        super(BookingsDetailedView, self).__init__(context, request)
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
            membership = getToolByName(context, 'portal_membership')
            member = membership.getAuthenticatedMember()
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

    @Lazy
    def toLocalizedTime(self):
        """Get the toLocalizedTime method from the plone view."""
        context = aq_inner(self.context)
        return context.restrictedTraverse('@@plone').toLocalizedTime

    def bookingbrain2extended_dict(self, bookingbrain):
        """Get a dict with extended info from this booking brain.

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

        # Webintelligenttext for the description
        desc = bookingbrain.Description
        pt = getToolByName(self.context, 'portal_transforms')
        desc = pt('web_intelligent_plain_text_to_html', desc)

        returnvalue = dict(
            booking_date = self.toLocalizedTime(bookingbrain.getBookingDate),
            day_of_week = bookingbrain.getBookingDate.Day(),
            project_title = project_title,
            task_url = taskbrain.getURL(),
            task_title = taskbrain.Title,
            # base_view of a booking gets redirected to the task view,
            # which we do not want here.
            booking_url = bookingbrain.getURL() + '/base_edit',
            booking_title = bookingbrain.Title,
            booking_description = desc,
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

    The period is actually a month, but the data is grouped by week.
    """

    def update(self):
        context = aq_inner(self.context)
        ptool = self.tools().properties()
        hours_per_day = ptool.xm_properties.getProperty('hours_per_day')
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
        month_billable = 0.0
        month_worked_days = 0

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
            week_total = 0.0
            week_strict_total = 0.0
            days_bookings = DayBookingOverview(
                context, request, memberid=self.memberid)
            week_billable = 0.0
            week_worked_days = 0
            # Strict billable means: only count days of this week that
            # are really in this month.
            week_strict_billable = 0.0
            week_strict_worked_days = 0
            while day_of_week < 7:
                day_total = days_bookings.raw_total(date=date)
                day_billable = days_bookings.raw_billable(date=date)
                ui_class = 'greyed'
                if day_total > 0:
                    # Update week stats
                    week_total += day_total
                    if day_total != 0:
                        # Only add the billable hours to the week when
                        # some work (billable or not) has been done
                        # today.
                        week_billable += day_billable
                        week_worked_days += 1
                    if date.month() == self.startDate.month():
                        # Update strict stats
                        week_strict_total += day_total
                        week_strict_billable += day_billable
                        week_strict_worked_days += 1
                        # Update month stats
                        self.raw_total += day_total
                        if day_total != 0:
                            # Only add the billable hours to the month
                            # when some work (billable or not) has
                            # been done today.
                            month_billable += day_billable
                            month_worked_days += 1
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
            weekinfo['week_total'] = formatTime(week_total)
            weekinfo['week_strict_total'] = formatTime(week_strict_total)
            # Normal week stats
            if week_worked_days:
                norm = week_worked_days * hours_per_day
                week_perc_billable = 100.0 * week_billable / norm
            else:
                week_perc_billable = 0.0
            fmt_perc_billable = "%0.1f %%" % week_perc_billable
            # Strict week stats
            if week_strict_worked_days:
                norm = week_strict_worked_days * hours_per_day
                week_strict_perc_billable = 100.0 * week_strict_billable / norm
            else:
                week_strict_perc_billable = 0.0
            fmt_strict_perc_billable = "%0.1f %%" % week_strict_perc_billable
            weekinfo['total_style'] = weekinfo['perc_style'] = 'greyed'
            if date < DateTime():
                weekinfo['total_style'] = weekinfo['perc_style'] = 'good'
                if week_total < 40.0:
                    weekinfo['total_style'] = 'not-enough'
                if week_perc_billable < 50:
                    weekinfo['perc_style'] = 'not-enough'
            weekinfo['perc_billable'] = fmt_perc_billable
            weekinfo['strict_perc_billable'] = fmt_strict_perc_billable
            self.bookinglist.append(weekinfo)

        if month_worked_days > 0:
            norm = month_worked_days * hours_per_day
            self.perc_billable = 100.0 * month_billable / norm


class YearBookingOverview(XMBaseView):
    request = None
    context = None
    months_list = []

    def __init__(self, context, request):
        super(YearBookingOverview, self).__init__(context, request)
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
        anno = IActualHours(context, None)
        if anno is not None:
            actual = anno.actual_time
        else:
            # What the???
            actual = -99.0
        ploneview = context.restrictedTraverse('@@plone')

        # Webintelligenttext for the description
        desc = context.Description()
        pt = getToolByName(context, 'portal_transforms')
        desc = pt('web_intelligent_plain_text_to_html', desc)

        returnvalue = dict(
            title = context.title_or_id(),
            description = desc,
            actual = formatTime(actual),
            booking_date = ploneview.toLocalizedTime(context.getBookingDate()),
            billable = context.getBillable(),
            creator = context.Creator(),
            # base_view of a booking gets redirected to the task view,
            # which we do not want here.
            url = context.absolute_url() + '/base_edit',
            )
        return returnvalue


class DayBookingOverview(XMBaseView):
    request = None
    context = None

    def __init__(self, context, request, memberid=None):
        super(DayBookingOverview, self).__init__(context, request)
        self.memberid = memberid or self.request.form.get('memberid')
        memberid = memberid or self.request.form.get('memberid')
        if self.memberid is None:
            mtool = self.tools().membership()
            member = mtool.getAuthenticatedMember()
            self.memberid = member.id
        self.searchpath = '/'.join(context.getPhysicalPath())

    def raw_billable(self, date=None):
        """return the total amount of billable hours"""
        date = date or self.request.form.get('date', DateTime().earliestTime())
        bookingbrains = self.tools().catalog().searchResults(
            portal_type='Booking',
            getBookingDate={"query": [date.earliestTime(), date.latestTime()],
                            "range": "minmax"},
            Creator=self.memberid,
            path=self.searchpath)
        billable=0.0
        for bb in bookingbrains:
            if bb.getBillable:
                billable += bb.actual_time
        return billable

    def billable(self, date=None):
        """return a percentage for billable hours"""
        context = aq_inner(self.context)
        ptool = self.tools().properties()
        hours_per_day = ptool.xm_properties.getProperty('hours_per_day')
        return (self.raw_billable(date) / hours_per_day) * 100

    def raw_total(self, date=None):
        """Raw total booked hours for a member for this date.
        """
        date = date or self.request.form.get('date', DateTime().earliestTime())
        bookingbrains = self.tools().catalog().searchResults(
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
