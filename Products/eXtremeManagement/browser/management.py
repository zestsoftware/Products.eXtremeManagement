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


class InvoicingView(XMBaseView):

    iteration_review_state = 'completed'

    def projectlist(self):
        context = aq_inner(self.context)
        searchpath = '/'.join(context.getPhysicalPath())
        # Get a list of all projects
        projectbrains = self.catalog.searchResults(portal_type='Project',
                                                   path=searchpath)

        for projectbrain in projectbrains:
            searchpath = projectbrain.getPath()
            # Search for Iterations that are ready to get invoiced
            iterationbrains = self.catalog.searchResults(
                portal_type='Iteration',
                review_state=self.iteration_review_state,
                path=searchpath)
            if len(iterationbrains) > 0:
                iteration_list = []
                for iterationbrain in iterationbrains:
                    info = self.iterationbrain2dict(iterationbrain)
                    iteration_list.append(info)
                info = self.projectbrain2dict(projectbrain)
                info['iterations'] = iteration_list
                yield info

    def iterationbrain2dict(self, brain):
        """Get a dict with info from this iteration brain.
        """
        review_state_id = brain.review_state
        estimate = brain.estimate
        actual = brain.actual_time
        obj = brain.getObject()
        history = self.workflow.getHistoryOf('eXtreme_Iteration_Workflow',
                                             obj)
        completion_date = None
        for item in history:
            if item['action'] == 'complete':
                completion_date = item['time']
        end_date = obj.getEndDate()
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
            completion_date = completion_date,
            end_date = end_date,
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


class InProgressView(InvoicingView):

    iteration_review_state = 'in-progress'
