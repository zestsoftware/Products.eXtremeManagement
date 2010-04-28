from Acquisition import aq_inner, aq_parent
from DateTime import DateTime
import logging
from plone.memoize.view import memoize
from Products.eXtremeManagement.browser.xmbase import XMBaseView
from Products.eXtremeManagement.utils import formatTime

logger = logging.getLogger('xm.listing')


class IterationListBaseView(XMBaseView):

    iteration_review_state = 'change_in_subclasses'
    billable_only = None

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

    @memoize
    def projectlist(self):
        context = aq_inner(self.context)
        searchpath = '/'.join(context.getPhysicalPath())
        # By default search for all projects from the given path
        # if the context is a project it will return itself
        cfilter = dict(portal_type='Project',
                       review_state='active',
                       path={'query': searchpath, 'navtree': False})
        if self.billable_only is not None:
            cfilter['getBillableProject'] = self.billable_only

        #portal = self.portal_state.portal()
        projectbrains = self.catalog.searchResults(cfilter)
        logger.info('%r projects found to iterate over' % len(projectbrains))

        results = []
        for projectbrain in projectbrains:
            searchpath = projectbrain.getPath()
            # Search for Iterations that are ready to get invoiced
            iterationbrains = self.catalog.searchResults(
                portal_type='Iteration',
                review_state=self.iteration_review_state,
                path={'query': searchpath, 'navtree': False})
            if len(iterationbrains) > 0:
                for iterationbrain in iterationbrains:
                    info = self.iterationbrain2dict(iterationbrain)
                    self.add_to_total(info)
                    info.update(self.projectbrain2dict(projectbrain))
                    results.append(info)
        return self.sort_results(results)

    def total(self):
        if self._total is None:
            # projectlist hasn't been called yet, so do it to
            # update the total.
            list(self.projectlist())
        return self._total

    @memoize
    def iterationbrain2dict(self, brain):
        """Get a dict with info from this iteration brain.
        """
        estimate = brain.estimate
        actual = brain.actual_time
        obj = brain.getObject()
        wf_id = 'eXtreme_Iteration_Workflow' # fallback
        wfs = self.workflow.getWorkflowsFor(obj)
        if len(wfs):
            wf_id = wfs[0].id
        history = self.workflow.getHistoryOf(wf_id, obj)
        completion_date = None
        for item in history:
            if item['action'] == 'complete':
                completion_date = item['time']
        returnvalue = dict(
            iteration_url = brain.getURL(),
            iteration_title = brain.Title,
            iteration_description = brain.Description,
            icon = brain.getIcon,
            man_hours = brain.getManHours,
            raw_estimate = estimate,
            estimate = formatTime(estimate),
            raw_actual = actual,
            actual = formatTime(actual),
            start_date = obj.getStartDate(),
            end_date = obj.getEndDate(),
            completion_date = completion_date,
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
    billable_only = True
    _invoiced_total = 0.0

    def sort_results(self, results):
        # allow sorting in subclasses by default on end_date of the iteration

        def sort_key(item):
            return item['end_date']

        results.sort(key=sort_key)

        return results

    def add_to_total(self, iteration_dict):
        if self._total is None:
            self._total = 0
        self._total += iteration_dict['raw_estimate']

    @memoize
    def total(self):
        if self._total is None:
            # projectlist hasn't been called yet, so do it to
            # update the total.
            self.projectlist()
        if self._total is None:
            # total could still be none if there are no iterations.
            return ''
        return '%.2f' % self._total

    @memoize
    def invoiced_total(self):
        if self._invoiced_total is None:
            # projectlist hasn't been called yet, so do it to
            # update the total.
            self.invoicedlist()
        if self._invoiced_total is None:
            # total could still be none if there are no iterations.
            return ''
        return '%.2f' % self._invoiced_total

    @memoize
    def invoicedlist(self):
        """ Return a list on invoiced iterations
        """
        # Search for Iterations that have been invoiced in the past month
        year = DateTime().year()
        month = DateTime().month()
        start_of_month = DateTime(year, month, 1)
        iterationbrains = self.catalog.searchResults(
            portal_type='Iteration',
            review_state='invoiced',
            modified={'query': start_of_month, 'range': 'min'},
            )
        results = []
        for iterationbrain in iterationbrains:
            info = self.iterationbrain2dict(iterationbrain)
            self._invoiced_total += float(iterationbrain.estimate)
            project = aq_parent(aq_inner(iterationbrain.getObject()))
            project_info = dict(url = project.absolute_url(),
                                title = project.Title(),
                                description = project.Description())
            info.update(project_info)
            results.append(info)

        return self.sort_results(results)


class InProgressView(IterationListBaseView):

    billable = 'billable'
    _actual = 0.0

    def sort_results(self, results):
        # sorting on end_date of the iteration

        def sort_key(item):
            return item['end_date']

        results.sort(key=sort_key)

        return results

    def add_to_total(self, iteration_dict):
        if self._total is None:
            self._total = 0.0
        self._total += float(iteration_dict['raw_estimate'])

    @memoize
    def total(self):
        if self._total is None:
            # projectlist hasn't been called yet, so do it to
            # update the total.
            self.projectlist()
        if self._total is None:
            # total could still be none if there are no iterations.
            return ''
        return '%.2f' % self._total

    @memoize
    def total_actual(self):
        if self._actual is None:
            # projectlist hasn't been called yet, so do it to
            # update the total.
            self.projectlist()
        if self._actual is None:
            # total could still be none if there are no iterations.
            return ''
        return '%.2f' % self._actual

    @memoize
    def viewing_billable(self):
        btype = self.request.get('type', 'billable')
        if btype == 'unbillable':
            return False
        return True

    def unbillable_url(self):
        return self.portal_state.portal_url() + '/inprogress?type=unbillable'

    def billable_url(self):
        return self.portal_state.portal_url() + '/inprogress?type=billable'

    @memoize
    def projectlist(self):
        """ Return a list on invoiced iterations
        """
        self.billable = self.request.get('type', 'billable')
        cfilter = dict(portal_type = 'Iteration',
                       review_state = 'in-progress',
                       getBillableProject = self.viewing_billable())
        iterationbrains = self.catalog.searchResults(cfilter)
        results = []
        for iterationbrain in iterationbrains:
            info = self.iterationbrain2dict(iterationbrain)
            self.add_to_total(info)
            self._actual += info['raw_actual']
            project = aq_parent(aq_inner(iterationbrain.getObject()))
            project_info = dict(url = project.absolute_url(),
                                title = project.Title(),
                                description = project.Description())
            info.update(project_info)
            results.append(info)

        return self.sort_results(results)
