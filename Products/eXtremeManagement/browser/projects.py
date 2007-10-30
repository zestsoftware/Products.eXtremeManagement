from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.eXtremeManagement.browser.xmbase import XMBaseView
from Products.eXtremeManagement.utils import formatTime
from Acquisition import aq_inner


class MyProjects(BrowserView):
    """Return the projects that I have tasks in.
    """
    request = None
    context = None
    states = ('open', 'to-do',)
    # Use state = '' if you do not want to filter for states.

    def projectlist(self):
        context = aq_inner(self.context)
        # Get a list of all projects
        catalog = getToolByName(context, 'portal_catalog')
        projectbrains = catalog.searchResults(portal_type='Project',)

        # Get the id of the currently logged in member
        membership = getToolByName(context, 'portal_membership')
        member = membership.getAuthenticatedMember()
        memberid = member.id
        plist = []
        for projectbrain in projectbrains:
            searchpath = projectbrain.getPath()
            taskbrains = catalog.searchResults(portal_type=['Task', 'PoiTask'],
                                               getAssignees=memberid,
                                               review_state=self.states,
                                               path=searchpath)

            if len(taskbrains) > 0:
                plist.append(projectbrain)

        return plist


class ProjectAdminView(XMBaseView):
    """Return management info about all projects.
    Specifically: which iterations can be invoiced.
    """

    def projectlist(self):
        context = aq_inner(self.context)
        searchpath = '/'.join(context.getPhysicalPath())
        # Get a list of all projects
        catalog = getToolByName(context, 'portal_catalog')
        projectbrains = catalog.searchResults(portal_type='Project',
                                              path=searchpath)

        plist = []
        for projectbrain in projectbrains:
            searchpath = projectbrain.getPath()
            # Search for Iterations that are ready to get invoiced
            iterationbrains = catalog.searchResults(portal_type='Iteration',
                                                    review_state='completed',
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
        context = aq_inner(self.context)
        review_state_id = brain.review_state
        workflow = getToolByName(context, 'portal_workflow')
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
            review_state_title = workflow.getTitleForStateOnType(
                                 review_state_id, 'Iteration'),
            brain= brain,
        )
        return returnvalue

    def projectbrain2dict(self, brain):
        """Get a dict with info from this project brain.
        """
        context = aq_inner(self.context)
        returnvalue = dict(
            url = brain.getURL(),
            title = brain.Title,
            description = brain.Description,
        )
        return returnvalue


class ProjectView(ProjectAdminView):
    """Simply return info about a Project.
    """

    def main(self):
        """Get a dict with info from this context.
        """
        context = aq_inner(self.context)
        workflow = getToolByName(context, 'portal_workflow')
        returnvalue = dict(
            title = context.Title(),
            description = context.Description(),
            url = context.absolute_url(),
            )
        return returnvalue

    def finished_iterations(self):
        states = ('completed','invoiced')
        return self.getIterations(states)

    def current_iterations(self):
        states = ('in-progress',)
        return self.getIterations(states)

    def open_iterations(self):
        states = ('new',)
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

    def non_iterations(self):
        """Return folder contents that are not iterations
        """
        context = aq_inner(self.context)
        filter = dict(portal_type='Iteration')
        iteration_brains = context.getFolderContents(filter)
        iteration_ids = [brain.id for brain in iteration_brains]
        all_brains = context.getFolderContents()
        brains = [brain for brain in all_brains
                  if brain.id not in iteration_ids]
        return brains
