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

    tasklist = []

    def __init__(self, context, request, year=None, month=None, memberid=None):
        super(TasksDetailedView, self).__init__(context, request)
        context = aq_inner(context)
        self.catalog = getToolByName(context, 'portal_catalog')
        self.xt = getToolByName(context, 'xm_tool')
        self.memberid = memberid or self.request.form.get('memberid')
        if self.memberid is None:
            member = context.portal_membership.getAuthenticatedMember()
            self.memberid = member.id


    def projects(self):
        context = aq_inner(self.context)
        searchpath = '/'.join(context.getPhysicalPath())

        projects = self.catalog.searchResults(portal_type='Project',
                                              path=searchpath)
        projectlist = []

        for project in projects:
            states = ('to-do',)
            searchpath = project.getPath()
            tasks = self.getOwnTasks(searchpath, states=states)
            if len(tasks) > 0:
                info = dict(project = project,
                            tasks = tasks,
                            totals = self.getTotalOwnTasks(tasks))
                projectlist.append(info)
        return projectlist

    def getOwnTasks(self, searchpath, states=None):
        filter = dict(states = states,
                      assignees = self.memberid,
                      searchpath = searchpath)
        return self.xt.getTasks(**filter)
        
    def myPortion(self, task):
        return 1.0/len(task.getAssignees)

    def getTotalOwnTasks(self, tasks):
        """Get my portion of total estimate, etc for these tasks
        """
        rawEstimate = sum([task.getRawEstimate * self.myPortion(task)
                           for task in tasks])
        rawActualHours = sum([task.getRawActualHours * self.myPortion(task)
                              for task in tasks])
        rawDifference = sum([task.getRawDifference * self.myPortion(task)
                             for task in tasks])
        return map(self.xt.formatTime, (rawEstimate, rawActualHours, rawDifference))
