from Products.CMFCore.utils import getToolByName


class MyProjects(object):
    """Return the projects that I have tasks in.
    """
    states = ('open', 'to-do',)
    # Use state = '' if you do not want to filter for states.

    def __init__(self, context, request=None):
        self.context = context
        if request is None:
            # At least handy for testing.
            self.request = self.context.REQUEST
        else:
            self.request = request
    
    def projectlist(self):
        # Get a list of all projects
        catalog = getToolByName(self.context, 'portal_catalog')
        projectbrains = catalog.searchResults(portal_type='Project',)

        # Get the id of the currently logged in member
        membership = getToolByName(self.context, 'portal_membership')
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
