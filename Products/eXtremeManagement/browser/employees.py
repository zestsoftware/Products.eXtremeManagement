import itertools
from datetime import date
from DateTime import DateTime
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser import BrowserView
from plone.memoize.view import memoize
from zope.interface import implements

from Products.eXtremeManagement.browser.bookings import WeekBookingOverview
try:
    from Products.eXtremeManagement.utils import getNextYearMonth
    from Products.eXtremeManagement.utils import getPrevYearMonth
    from Products.eXtremeManagement.utils import getEndOfMonth
except ImportError:
    # BBB for Products.eXtremeManagement before 2.0 alpha 3
    from Products.eXtremeManagement.browser.bookings import getNextYearMonth
    from Products.eXtremeManagement.browser.bookings import getPrevYearMonth
    from Products.eXtremeManagement.browser.bookings import getEndOfMonth

from xm.theme import xmMessageFactory as _
from interfaces import IEmployeesView


def booking_date(brain):
    return brain.getBookingDate.earliestTime()


def fmt_perc_billable(perc):
    return "%0.1f" % perc + ' %'


class EmployeesView(BrowserView):
    """Return information about the contents of a project."""
    implements(IEmployeesView)

    def __init__(self, context, request, year=None):
        self.context = context
        self.request = request
        portal_url = getToolByName(context, 'portal_url')
        self.portal = portal_url.getPortalObject()
        self.site_url = portal_url()
        self.catalog = getToolByName(context, 'portal_catalog')
        self.mtool = getToolByName(context, 'portal_membership')
        self.searchpath = '/'.join(context.getPhysicalPath())
        today = date.today()
        self.months = []
        # months is a list of date objects of the past 12 months
        # counting backwards from now.
        m = today.month
        y = today.year
        for x in range(12):
            self.months.append(date(y, m, 1))
            m = m - 1
            if m <= 0:
                m += 12
                y -= 1

    @memoize
    def items(self):
        context = aq_inner(self.context)
        propstool = getToolByName(context, 'portal_properties')
        hours_per_day = propstool.xm_properties.getProperty('hours_per_day')
        data = []
        employees = self.get_employees()
        for userid in employees:
            empldict = {}
            memberinfo = self.mtool.getMemberInfo(userid)
            if memberinfo and memberinfo is not None:
                empldict['name'] = memberinfo['fullname']
                # For each month create a list employees in a dict with
                # percentages and a url to the month view.
                results = []
                for m in self.months:
                    begin = DateTime(m.year, m.month, 1)
                    end = getEndOfMonth(m.year, m.month)
                    bookingbrains = self.catalog.searchResults(
                        portal_type='Booking',
                        getBookingDate={"query": [begin, end],
                                        "range": "minmax",
                                        "sort_on": "getBookingDate"},
                        Creator=userid,
                        path=self.searchpath)
                    # Hm, it does not look like sort_on is working so
                    # we do it ourselves.
                    bookingbrains = sorted(bookingbrains, key=booking_date)
                    grouped = itertools.groupby(bookingbrains, booking_date)
                    billable = []
                    for day, bookings in grouped:
                        day_billable = 0.0
                        day_total = 0.0
                        for bb in bookings:
                            day_total += bb.actual_time
                            if bb.getBillable:
                                day_billable += bb.actual_time
                        # XXX Turn this into 1 hour.
                        if day_total > 0:
                            # If the employee worked 1 hour or less we
                            # assume it is just an hour on Saturday or
                            # something and we ignore this day to
                            # avoid unnecessarily influencing the
                            # billable percentage negatively.  If he
                            # worked more, we assume it is a full day.
                            billable.append(day_billable)
                    days_worked = len(billable)
                    if days_worked > 0:
                        total = sum(billable)
                        perc = 100 * (total / hours_per_day) / days_worked
                    else:
                        perc = 0.0
                    url = "%s/booking_month?memberid=%s&month=%r&year=%r" % (
                        self.site_url, userid, m.month, m.year)
                    perc_dict = dict(percentage = fmt_perc_billable(perc),
                                     url = url)
                    results.append(perc_dict)
                results.reverse()
                empldict['monthly_percentages'] = results
            data.append(empldict)

        return data

    @memoize
    def olditems(self):
        context = aq_inner(self.context)
        data = []
        employees = self.get_employees()
        for userid in employees:
            empldict = {}
            memberinfo = self.mtool.getMemberInfo(userid)
            if memberinfo and memberinfo is not None:
                empldict['name'] = memberinfo['fullname']
                # For each month create a list employees in a dict with
                # percentages and a url to the month view.
                results = []
                for m in self.months:
                    opts = dict(year=m.year, month=m.month, memberid=userid)
                    view = WeekBookingOverview(context, self.request,
                                               **opts)
                    val = view.main()
                    url = "%s/booking_month?memberid=%s&month=%r&year=%r" % \
                                                (self.site_url, userid,
                                                m.month, m.year)
                    perc_dict = dict(percentage = val['perc_billable'],
                                   url = url)
                    results.append(perc_dict)
                results.reverse()
                empldict['monthly_percentages'] = results
            data.append(empldict)

        return data

    @memoize
    def month_names(self):
        """ Return a list of translated month names used for the header of the
        table.
        """
        results = []
        for m in self.months:
            month = _(safe_unicode(m.strftime('%B')))
            year = safe_unicode(str(m.year))
            results.append(' '.join([month, year]))
        results.reverse()
        return results

    @memoize
    def get_employees(self):
        """return a list of userids which have a global role 'Employee'
        assigned.
        """
        employees = []
        acl_users = self.portal.acl_users
        roleman = acl_users.portal_role_manager
        for userid, loginname in roleman.listAssignedPrincipals('Employee'):
            if acl_users.getUser(userid):
                employees.append(userid)
        employees.sort()
        return employees
