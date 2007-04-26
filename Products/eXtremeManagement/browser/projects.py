from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.eXtremeManagement.browser.xmbase import XMBaseView
from Acquisition import aq_inner


class MyProjects(BrowserView):
    """Return the projects that I have tasks in.
    """
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
            taskbrains = catalog.searchResults(portal_type='Task',
                                               getAssignees=memberid,
                                               review_state=self.states,
                                               path=searchpath)

            if len(taskbrains) > 0:
                plist.append(projectbrain)

        return plist


class ProjectView(XMBaseView):
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

    def iterationbrain2dict(self, brain):
        """Get a dict with info from this iteration brain.
        """
        context = aq_inner(self.context)
        review_state_id = brain.review_state
        workflow = getToolByName(context, 'portal_workflow')
        returnvalue = dict(
            url = brain.getURL(),
            title = brain.Title,
            description = brain.Description,
            review_state = review_state_id,
            review_state_title = workflow.getTitleForStateOnType(
                                 review_state_id, 'Iteration'),
            icon = brain.getIcon,
            man_hours = brain.getManHours,
            actual = self.xt.formatTime(brain.getRawActualHours),
            brain = brain,
        )
        return returnvalue
