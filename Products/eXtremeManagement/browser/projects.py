from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from zope.cachedescriptors.property import Lazy
from plone.memoize.view import memoize
from kss.core import kssaction
from plone.app.kss.plonekssview import PloneKSSView
from zope.component import getMultiAdapter
from datetime import date, timedelta
import time
from DateTime import DateTime

try:
    import xm.theme
except ImportError:
    HAS_XM_THEME = False
else:
    HAS_XM_THEME = True


from Products.eXtremeManagement.browser.xmbase import XMBaseView
from Products.eXtremeManagement.utils import formatTime


class Projects(XMBaseView):
    """Manage all projects.
    """

    @memoize
    def iterationsforproject(self, projectbrain):
        searchpath = projectbrain.getPath()
        # Search for Iterations that are ready to get invoiced
        return self.catalog.searchResults(portal_type='Iteration',
                                                     path=searchpath)

    @memoize
    def projects(self):
        return self.catalog.searchResults(portal_type='Project',
                                          review_state='active')


class Scheduling(Projects):
    """Pan-project scheduling"""

    weekcount = 14 # Number of weeks to display
    weekpreroll = 2 # Number of weeks to show *before* the desired starting date
    # Displayed width in pixels - declared here so we can calculate iteration
    # positions in code
    cellwidth = 16

    def datetotimestamp(self, dateobj):
        return int(time.mktime(dateobj.timetuple()))

    def displayrange(self):
        return timedelta(self.weekcount*7)

    def startingtimestamp(self):
        try:
            start = int(self.request.get('start'))
        except TypeError:
            start = int(time.time())
        return start

    def startingdate(self, stamp=None):
        stamp = stamp or self.startingtimestamp()
        start = date.fromtimestamp(stamp)
        monday = start - timedelta(self.weekpreroll*7)
        while monday.weekday() != 0:
            monday -= timedelta(1)
        return monday

    def endingdate(self):
        return self.startingdate() + self.displayrange()

    def currentweek(self):
        """Calculate the first day of the current week"""
        monday = date.today()
        while monday.weekday() != 0:
            monday -= timedelta(1)
        return monday

    def schedule_weeks(self):
        """
        Calculate the day range to display in the schedule view, showing the
        weeks before and after the current date.
        """
        monday = self.startingdate()
        return [monday + timedelta(i*7) for i in range(self.weekcount)]

    def iterationsforproject(self, projectbrain):
        """Filter iterations based on the current date range and build a data
        structure useful to the JavaScript interface"""
        sdate = self.datetotimestamp(self.startingdate())
        edate = self.datetotimestamp(self.endingdate())
        iterations = []
        for iterationbrain in Projects.iterationsforproject(self, projectbrain):
            iteration = iterationbrain.getObject()
            try:
                start = float(iteration.startDate)
                end = float(iteration.endDate)
                if sdate < start and end < edate:
                    iterations.append(dict(
                        uid = iteration.UID,
                        title = iteration.Title(),
                        # only unstarted iterations can be moved...
                        movable = time.time() < start,
                        start = int((start - sdate) / 60 / 60 / 24)  * self.cellwidth,
                        period = int((end - start) / 60 / 60 / 24) * self.cellwidth,
                    ))
            except TypeError:
                pass # Probably empty iteration dates
        return iterations


class MoveIteration(PloneKSSView):
    """Respond to a KSS request to move an iteration to a new start day"""

    @kssaction
    def move_iteration(self, uid, daystart, dayoffset):
        """Find an iteration by uid and move it to a new start day"""
        print 'move_iteration', uid, date.fromtimestamp(int(daystart)), dayoffset
        # Sanitise the daystart
        view = self.context.restrictedTraverse('@@scheduling')
        first_day = view.startingdate(stamp=int(daystart))
        # Set start date of iteration with UID 'uid' to first_day + dayoffset
        newd = first_day + timedelta(int(dayoffset))
        uid_catalog = getToolByName(self.context, 'uid_catalog')
        brain = uid_catalog(UID=uid)[0]
        obj = brain.getObject()
        duration = obj.duration()
        obj.startDate = DateTime(newd.year, newd.month, newd.day)
        # Maintain duration of iteration by setting endDate too
        obj.endDate = obj.startDate + duration

class MyProjects(XMBaseView):
    """Return the projects that I have tasks in.
    """
    request = None
    context = None

    @property
    @memoize
    def projectlist(self):
        context = aq_inner(self.context)
        # Get a list of all projects
        projectbrains = self.catalog.searchResults(portal_type='Project',
                                                   review_state='active')

        if len(projectbrains) <= 1:
            # If there is maximal 1 project: return it...
            return projectbrains
        else:
            # ... otherwise filter them.
            membership = getToolByName(context, 'portal_membership')
            member = membership.getAuthenticatedMember()
            memberid = member.id

            # Customers see all their projects (which should be a
            # limited number anyway).
            # Quick'n'Dirty check: pick the first project and check
            # whether the user has the customer role, but is not an
            # employee.
            # ProjectManagers and Manager also get the entire list of active
            # projects
            projectbrain = projectbrains[0]
            roles = member.getRolesInContext(projectbrain.getObject())
            if 'ProjectManager' in roles or 'Manager' in roles or \
                'Customer' in roles and 'Employee' not in roles:
                return projectbrains

            # Otherwise only show the projects with open tasks assigned to
            # this user.
            plist = []
            states = ('open', 'to-do')
            for projectbrain in projectbrains:
                searchpath = projectbrain.getPath()
                taskbrains = self.catalog.searchResults(portal_type=['Task',
                                                                'PoiTask'],
                                                   getAssignees=memberid,
                                                   review_state=states,
                                                   path=searchpath)
                if len(taskbrains) > 0:
                    plist.append(projectbrain)
            return plist


class ProjectView(XMBaseView):
    """Simply return info about a Project.
    """

    def projectlist(self):
        context = aq_inner(self.context)
        searchpath = '/'.join(context.getPhysicalPath())
        # Get a list of all projects
        projectbrains = self.catalog.searchResults(portal_type='Project',
                                              path=searchpath)

        plist = []
        for projectbrain in projectbrains:
            searchpath = projectbrain.getPath()
            # Search for Iterations that are ready to get invoiced
            iterationbrains = self.catalog.searchResults(
                portal_type='Iteration', review_state='completed',
                path=searchpath)
            if len(iterationbrains) > 0:
                iteration_list = []
                for iterationbrain in iterationbrains:
                    info = self.iterationbrain2dict(iterationbrain)
                    iteration_list.append(info)
                info = dict(project = self.projectbrain2dict(projectbrain),
                            iterations = iteration_list)
                plist.append(info)
        return plist

    def iterationbrain2dict(self, brain):
        """Get a dict with info from this iteration brain.
        """
        review_state_id = brain.review_state
        estimate = brain.estimate
        actual = brain.actual_time
        returnvalue = dict(
            url = brain.getURL(),
            title = brain.Title,
            description = brain.Description,
            icon = brain.getIcon,
            man_hours = brain.getManHours,
            estimate = formatTime(estimate),
            actual = formatTime(actual),
            difference = formatTime(estimate - actual),
            review_state = review_state_id,
            review_state_title = self.workflow.getTitleForStateOnType(
                                 review_state_id, 'Iteration'),
            brain= brain,
        )
        return returnvalue

    def projectbrain2dict(self, brain):
        """Get a dict with info from this project brain.
        """
        returnvalue = dict(
            url = brain.getURL(),
            title = brain.Title,
            description = brain.Description,
        )
        return returnvalue


    def main(self):
        """Get a dict with info from this context.
        """
        context = aq_inner(self.context)
        returnvalue = dict(
            title = context.Title(),
            description = context.Description(),
            url = context.absolute_url(),
            )
        return returnvalue

    def current_iterations(self):
        states = ('in-progress', )
        return self.getIterations(states)

    def getIterations(self, states=None):
        """Return the iterations, in catalog form

        Parameters:
        states: Iterations with these states will be returned.
                If None, all are returned.
        """
        context = aq_inner(self.context)
        filter = dict(portal_type='Iteration',
                      review_state=states)
        brains = context.getFolderContents(filter)
        iteration_list = []
        for brain in brains:
            info = self.iterationbrain2dict(brain)
            iteration_list.append(info)
        return iteration_list

    def show_attachments(self):
        """Should attachments be shown?

        Not when there are no attachments and also not when xm.theme
        is installed as the attachments can be seen in portlets then.
        """
        if HAS_XM_THEME:
            return False
        return len(self.attachments) != 0

    @Lazy
    def attachments(self):
        """Return folder contents that are not iterations or offers
        """
        context = aq_inner(self.context)
        cfilter = dict(portal_type=('Iteration',
                                    'Offer'))
        iteration_brains = context.getFolderContents(cfilter)
        iteration_ids = [brain.id for brain in iteration_brains]
        all_brains = context.getFolderContents()
        brains = [brain for brain in all_brains
                  if brain.id not in iteration_ids]
        return brains

    def offers(self):
        """Return list of dicts with the title and url to the offers inside a
        project.
        """
        context = aq_inner(self.context)
        cfilter = dict(portal_type='Offer')
        offer_brains = context.getFolderContents(cfilter)
        results = []
        if offer_brains:
            plone_view = getMultiAdapter((context, self.request),
                                         name=u'plone')
            icon = plone_view.getIcon(offer_brains[0].getObject())
            for offer in offer_brains:
                results.append(dict(brain = offer,
                                    title = offer.Title,
                                    url = offer.getURL,
                                    icon = icon.html_tag()))
        return results
