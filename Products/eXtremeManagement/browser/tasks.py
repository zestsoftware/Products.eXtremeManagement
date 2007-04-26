from Products.CMFCore.utils import getToolByName
from Products.eXtremeManagement.browser.xmbase import XMBaseView
from Products.Five.browser import BrowserView
from Acquisition import aq_inner


class TaskView(XMBaseView):
    """Simply return info about a Task.
    """
 
    def main(self):
        """Get a dict with info from this Task.
        """
        workflow = getToolByName(self.context, 'portal_workflow')
        returnvalue = dict(
            title = self.context.Title(),
            description = self.context.Description(),
            cooked_body = self.context.CookedBody(),
            estimate = self.xt.formatTime(self.context.getRawEstimate()),
            actual = self.xt.formatTime(self.context.getRawActualHours()),
            difference = self.xt.formatTime(self.context.getRawDifference()),
            review_state = workflow.getInfoFor(self.context, 'review_state'),
            assignees = self.context.getAssignees(),
            )
        return returnvalue

    def bookings(self):
        current_path = '/'.join(self.context.getPhysicalPath())
        catalog = getToolByName(self.context, 'portal_catalog')
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
        returnvalue = dict(
            date = self.context.restrictedTraverse('@@plone').toLocalizedTime(brain.getBookingDate),
            # base_view of a booking gets redirected to the task view,
            # which we do not want here.
            url = brain.getURL() + '/base_edit',
            title = brain.Title,
            description = brain.Description,
            actual = self.xt.formatTime(brain.getRawActualHours),
            creator = brain.Creator,
            billable = brain.getBillable,
        )
        return returnvalue


class TasksDetailedView(BrowserView):
    """Return a list of Tasks.
    """

    default_state = 'to-do'
    possible_states = []

    def __init__(self, context, request, state=None, memberid=None):
        super(TasksDetailedView, self).__init__(context, request)
        context = aq_inner(context)
        self.catalog = getToolByName(context, 'portal_catalog')
        self.xt = getToolByName(context, 'xm_tool')
        self.memberid = memberid or self.request.form.get('memberid')
        if self.memberid is None:
            member = context.portal_membership.getAuthenticatedMember()
            self.memberid = member.id
        self.state = state or self.request.form.get('state', self.default_state)
        self.possible_states = ['open', 'to-do', 'completed']
        try:
            self.possible_states.remove(self.state)
        except ValueError:
            # State is not known to us.
            pass

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

    def tasklist(self, searchpath=None):
        if searchpath is None:
            context = aq_inner(self.context)
            searchpath = '/'.join(context.getPhysicalPath())

        tasks = self.getOwnTasks(searchpath)
        info = dict(tasks = tasks,
                    totals = self.getTotalOwnTasks(tasks))
        return info

    def simple_tasklist(self):
        context = aq_inner(self.context)
        searchpath = '/'.join(context.getPhysicalPath())
        return self.getOwnTasks(searchpath)

    def getOwnTasks(self, searchpath):
        filter = dict(states = self.state,
                      assignees = self.memberid,
                      searchpath = searchpath)
        return self.xt.getTasks(**filter)
        
    def getTotalOwnTasks(self, tasks):
        """Get my portion of total estimate, etc for these tasks
        """
        rawEstimate = sum([task.getRawEstimate / len(task.getAssignees)
                           for task in tasks])
        rawActualHours = sum([task.getRawActualHours / len(task.getAssignees)
                              for task in tasks])
        rawDifference = sum([task.getRawDifference / len(task.getAssignees)
                             for task in tasks])
        totals = dict(
            estimate = self.xt.formatTime(rawEstimate),
            actual = self.xt.formatTime(rawActualHours),
            difference = self.xt.formatTime(rawDifference),
            )
        return totals

class EmployeeTotalsView(BrowserView):
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
        taskbrains = self.xt.getTasks(**filter)

        memberlist = []
        members = context.getProject().getMembers()
        for memberid in members:
            tasks = [taskbrain for taskbrain in taskbrains
                     if memberid in taskbrain.getAssignees]
            rawEstimate = sum([task.getRawEstimate / len(task.getAssignees)
                               for task in tasks])
            if rawEstimate > 0:
                bookings = self.catalog.searchResults(
                    portal_type='Booking',
                    Creator=memberid,
                    path=searchpath)
                rawActualHours = sum([booking.getRawActualHours for booking in bookings])
                rawDifference = rawEstimate - rawActualHours
                info = dict(
                    memberid = memberid,
                    estimate = self.xt.formatTime(rawEstimate),
                    actual = self.xt.formatTime(rawActualHours),
                    difference = self.xt.formatTime(rawDifference),
                    )
                memberlist.append(info)
        return memberlist
