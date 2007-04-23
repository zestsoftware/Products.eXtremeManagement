from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.eXtremeManagement.browser.xmbase import XMBaseView
from Acquisition import aq_inner


class MyProjects(BrowserView):
    """Return the projects that I have tasks in.
    """
    states = ('open', 'to-do',)
    # Use state = '' if you do not want to filter for states.

    def __init__(self, context, request):
        self.context = context
        self.request = request
    
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
            url = projectbrain.getURL()
            searchpath = '/'.join(self.request.physicalPathFromURL(url))
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
        return self.getIterations(('completed','invoiced',))

    def current_iterations(self):
        return self.getIterations(('in-progress',))

    def open_iterations(self):
        return self.getIterations(('new',))

    def getIterations(self, states=None):
        """Return the iterations, in catalog form

        Parameters:
        states: Iterations with these states will be returned.
        """

        context = aq_inner(self.context)

        brains = context.getFolderContents({'portal_type':'Iteration'})

        iteration_list = []
        if states is None:
            list = brains
        else:
            for brain in brains:
                if brain.review_state in states:
                    iteration_list.append(brain)

        return iteration_list
