from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from zope.cachedescriptors.property import Lazy
from plone.memoize.view import memoize
from zope.component import getMultiAdapter
try:
    import xm.theme
except ImportError:
    HAS_XM_THEME = False
else:
    HAS_XM_THEME = True


from Products.eXtremeManagement.browser.xmbase import XMBaseView
from Products.eXtremeManagement.utils import formatTime


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
