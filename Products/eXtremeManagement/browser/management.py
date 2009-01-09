from Acquisition import aq_inner
from zope import component

from Products.eXtremeManagement.browser.xmbase import XMBaseView
from Products.eXtremeManagement.utils import formatTime


class IterationListBaseView(XMBaseView):

    iteration_review_state = 'change_in_subclasses'
    _total = None

    def sort_results(self, results):
        # allow sorting in subclasses
        return results

    def add_to_total(self, iteration_dict):
        """Increase total with this iteration's value"""
        pass

    def extra_dict(self, obj, brain):
        """Add additional information to the iterationdict."""
        return {}

    def projectlist(self):
        context = aq_inner(self.context)
        searchpath = '/'.join(context.getPhysicalPath())
        # By default search for all projects from the given path
        # if the context is a project it will return itself
        cfilter = dict(portal_type='Project',
                       getBillableProject=True,
                       path={'query': searchpath, 'navtree': False})
        # Get a list of all 'active' projects in case the context is the portal
        # This will narrow down de number of results and improve performance.
        portal_state = component.getMultiAdapter((self.context, self.request),
                                                 name=u'plone_portal_state')
        portal = portal_state.portal()
        if context == portal:
            cfilter['review_state'] = 'active'
        projectbrains = self.catalog.searchResults(cfilter)

        for projectbrain in projectbrains:
            searchpath = projectbrain.getPath()
            # Search for Iterations that are ready to get invoiced
            iterationbrains = self.catalog.searchResults(
                portal_type='Iteration',
                review_state=self.iteration_review_state,
                path={'query': searchpath, 'navtree': False})
            if len(iterationbrains) > 0:
                iteration_list = []
                for iterationbrain in iterationbrains:
                    info = self.iterationbrain2dict(iterationbrain)
                    self.add_to_total(info)
                    iteration_list.append(info)
                info = self.projectbrain2dict(projectbrain)
                info['iterations'] = self.sort_results(iteration_list)
                yield info

    def total(self):
        if self._total is None:
            # projectlist hasn't been called yet, so do it to
            # update the total.
            list(self.projectlist())
        return self._total

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
            start_date = obj.getStartDate(),
            completion_date = completion_date,
            end_date = end_date,
            brain= brain,
        )
        returnvalue.update(self.extra_dict(obj, brain))
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


class InvoicingView(IterationListBaseView):

    iteration_review_state = 'completed'


class InProgressView(IterationListBaseView):

    iteration_review_state = 'in-progress'
