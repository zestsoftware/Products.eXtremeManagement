import datetime
from Acquisition import aq_inner

from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView

from Products.eXtremeManagement.browser.xmbase import XMBaseView
from Products.eXtremeManagement.timing.interfaces import IActualHours
from Products.eXtremeManagement.timing.interfaces import IEstimate


class TaskView(XMBaseView):
    """Simply return info about a Task.
    """

    def __init__(self, context, request):
        super(TaskView, self).__init__(context, request)

        propstool = getToolByName(context, 'portal_properties')
        self.friendlyDateFormat = \
            propstool.site_properties.getProperty('friendlyDateFormat', None)

    def main(self):
        """Get a dict with info from this Task.
        """
        context = aq_inner(self.context)
        workflow = getToolByName(self.context, 'portal_workflow')
        anno = IActualHours(context, None)
        if anno is not None:
            actual = anno.actual_time
        else:
            # Should not happen (tm).
            actual = -99.0
        est = IEstimate(context, None)
        if est is not None:
            estimate = est.estimate
        else:
            # Should not happen (tm).
            estimate = -99.0
        returnvalue = dict(
            title = context.Title(),
            description = context.Description(),
            cooked_body = context.CookedBody(),
            estimate = self.xt.formatTime(estimate),
            actual = self.xt.formatTime(actual),
            difference = self.xt.formatTime(estimate - actual),
            review_state = workflow.getInfoFor(context, 'review_state'),
            assignees = [{'niceName': context.poi_niceName(username=x),
                          'username': x,
                          'active': True}
                         for x in context.getAssignees()],
            )
        return returnvalue

    def bookings(self):
        context = aq_inner(self.context)
        current_path = '/'.join(context.getPhysicalPath())
        catalog = getToolByName(context, 'portal_catalog')
        bookingbrains = catalog.searchResults(portal_type='Booking',
                                              sort_on='getBookingDate',
                                              path=current_path)
        booking_list = []

        for bookingbrain in bookingbrains:
            info = self.bookingbrain2dict(bookingbrain)
            booking_list.append(info)

        return booking_list

    def bookingbrain2dict(self, brain):
        """Get a dict with info from this booking brain.
        """
        context = aq_inner(self.context)

        realDate = brain.getBookingDate

        ploneview = context.restrictedTraverse('@@plone')
        date = ploneview.toLocalizedTime(realDate, self.friendlyDateFormat)

        today = datetime.date.today()
        pyDate = datetime.date(realDate.year(), realDate.month(),
                               realDate.day())
        if today == pyDate:
            date = 'Today (%s)' % date
        elif (pyDate - today).days == -1:
            date = 'Yesterday (%s)' % date

        returnvalue = dict(
            date = date,
            # base_view of a booking gets redirected to the task view,
            # which we do not want here.
            url = brain.getURL() + '/base_edit',
            title = brain.Title,
            description = brain.Description,
            actual = self.xt.formatTime(brain.actual_time),
            creator = brain.Creator,
            billable = brain.getBillable,
        )
        return returnvalue


class TasksDetailedView(BrowserView):
    """Return a list of Tasks for everyone with all states.
    """

    def __init__(self, context, request):
        super(TasksDetailedView, self).__init__(context, request)
        context = aq_inner(context)
        self.catalog = getToolByName(context, 'portal_catalog')
        self.xt = getToolByName(context, 'xm_tool')
        self.filter = dict(portal_type=['Task', 'PoiTask'],
                           sort_on='getObjPositionInParent')

    def simple_tasklist(self, searchpath=None, sort_by_state=False):
        """Get some tasks.
        """
        if searchpath is None:
            context = aq_inner(self.context)
            searchpath = '/'.join(context.getPhysicalPath())
        filter = self.filter
        filter['path'] = searchpath
        items = self.catalog.searchResults(**filter)
        if filter.get('review_state') or not sort_by_state:
            # We do not want to sort by state or we filter for review
            # state already, so we can simply return the items.
            return items
        else:
            # First sort the items by state (next to possible other sort)
            return self.xt.getStateSortedContents(items)

    def tasklist(self, searchpath=None, sort_by_state=False):
        brains = self.simple_tasklist(searchpath, sort_by_state)
        task_list = []
        for brain in brains:
            info = self.taskbrain2dict(brain)
            task_list.append(info)
        if not sort_by_state:
            task_list.sort(
                lambda a, b: cmp(a['story_title'], b['story_title']) or
                             cmp(a['title'], b['title'])
                )
        info = dict(tasks = task_list,
                    totals = self.getTaskTotals(brains))
        return info
        
    def portion(self, task):
        """What portion of a task should be added to the total?
        Specifically: should we adjust for the number of assignees?
        In this view: no.
        """
        return 1.0

    def getTaskTotals(self, tasks):
        """Get my portion of total estimate, etc for these tasks
        """
        rawEstimate = sum([task.estimate * self.portion(task)
                           for task in tasks])
        rawActualHours = sum([task.actual_time * self.portion(task)
                              for task in tasks])
        rawDifference = sum([(task.estimate - task.actual_time)
                             * self.portion(task) for task in tasks])
        totals = dict(
            estimate = self.xt.formatTime(rawEstimate),
            actual = self.xt.formatTime(rawActualHours),
            difference = self.xt.formatTime(rawDifference),
            )
        return totals

    def taskbrain2dict(self, brain):
        """Get a dict with info from this task brain.
        """
        context = aq_inner(self.context)
        review_state_id = brain.review_state
        workflow = getToolByName(context, 'portal_workflow')

        # Get info about parent Story
        parentPath = '/'.join(brain.getPath().split('/')[:-1])
        filter = dict(portal_type='Story', path=parentPath)
        storybrain = self.catalog(**filter)[0]

        estimate = brain.estimate
        actual = brain.actual_time
        returnvalue = dict(
            url = brain.getURL(),
            UID = brain.UID,
            title = brain.Title,
            story_url = storybrain.getURL(),
            story_title = storybrain.Title,
            description = brain.Description,
            estimate = self.xt.formatTime(estimate),
            actual = self.xt.formatTime(actual),
            difference = self.xt.formatTime(estimate - actual),
            review_state = review_state_id,
            review_state_title = workflow.getTitleForStateOnType(
                                 review_state_id, 'Task'),
            assignees = brain.getAssignees,
        )
        return returnvalue


class MyTasksDetailedView(TasksDetailedView):
    """Return a list of Tasks in a specific state that I am assigned to.
    """

    state = 'to-do'
    possible_states = []

    def __init__(self, context, request, state=None, memberid=None):
        super(MyTasksDetailedView, self).__init__(context, request)
        context = aq_inner(context)
        self.memberid = memberid or self.request.form.get('memberid')
        if self.memberid is None:
            member = context.portal_membership.getAuthenticatedMember()
            self.memberid = member.id
        self.state = state or self.request.form.get('state', self.state)
        self.possible_states = ['open', 'to-do', 'completed']
        try:
            self.possible_states.remove(self.state)
        except ValueError:
            # State is not known to us.
            # Might be 'all' since we treat that specially.
            pass
        self.filter = dict(
            portal_type = ['Task', 'PoiTask'],
            getAssignees = self.memberid,
            review_state = self.state,
            sort_on='getObjPositionInParent',
            )

    def projects(self):
        context = aq_inner(self.context)
        searchpath = '/'.join(context.getPhysicalPath())

        projects = self.catalog.searchResults(portal_type='Project',
                                              path=searchpath)
        projectlist = []

        for project in projects:
            searchpath = project.getPath()
            info = self.tasklist(searchpath)
            if len(info['tasks']) > 0:
                info['project'] = project
                projectlist.append(info)
        return projectlist

    def portion(self, task):
        """What portion of a task should be added to the total?
        Specifically: should we adjust for the number of assignees?
        In this view: yes.
        """
        return 1.0 / len(task.getAssignees)


class EmployeeTotalsView(TasksDetailedView):
    """Return an overview for employees
    """

    def __init__(self, context, request):
        super(EmployeeTotalsView, self).__init__(context, request)
        context = aq_inner(context)
        self.catalog = getToolByName(context, 'portal_catalog')
        self.xt = getToolByName(context, 'xm_tool')

    def totals(self):
        context = aq_inner(self.context)
        searchpath = '/'.join(context.getPhysicalPath())

        filter = dict(searchpath = searchpath)
        taskbrains = self.simple_tasklist(**filter)

        memberlist = []
        members = context.getProject().getMembers()
        for memberid in members:
            tasks = [taskbrain for taskbrain in taskbrains
                     if memberid in taskbrain.getAssignees]
            rawEstimate = sum([task.estimate / len(task.getAssignees)
                               for task in tasks])
            bookings = self.catalog.searchResults(
                portal_type='Booking',
                Creator=memberid,
                path=searchpath)
            rawActualHours = sum([booking.actual_time for booking in bookings])
            if rawEstimate > 0 or rawActualHours > 0:
                rawDifference = rawEstimate - rawActualHours
                info = dict(
                    memberid = memberid,
                    estimate = self.xt.formatTime(rawEstimate),
                    actual = self.xt.formatTime(rawActualHours),
                    difference = self.xt.formatTime(rawDifference),
                    )
                memberlist.append(info)

        return memberlist
