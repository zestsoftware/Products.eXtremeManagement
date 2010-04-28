from Acquisition import aq_inner
from plone.memoize.view import memoize
from Products.eXtremeManagement.utils import formatTime
from Products.eXtremeManagement.browser.xmbase import XMBaseView


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

    @memoize
    def projectlist(self):
        context = aq_inner(self.context)
        results = []
        searchpath = '/'.join(context.getPhysicalPath())
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
            info = self.projectdict()
            info['iterations'] = self.sort_results(iteration_list)
            results.append(info)
        return results

    @memoize
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
        returnvalue = dict(
            url = brain.getURL(),
            title = brain.Title,
            description = brain.Description,
            raw_estimate = estimate,
            estimate = formatTime(estimate),
            actual = formatTime(actual),
            review_state = review_state_id,
            review_state_title = self.workflow.getTitleForStateOnType(
                                 review_state_id, 'Iteration'),
            start_date = obj.getStartDate(),
            end_date = obj.getEndDate(),
            completion_date = completion_date,
            brain= brain,
        )
        returnvalue.update(self.extra_dict(obj, brain))
        return returnvalue

    @memoize
    def projectdict(self):
        """Get a dict with info from this project brain.
        """
        returnvalue = dict(
            url = self.context.absolute_url(),
            title = self.context.Title,
            description = self.context.Description,
        )
        return returnvalue


class FinishedIterationsView(IterationListBaseView):

    iteration_review_state = ['completed', 'invoiced', 'own-account']

    def add_to_total(self, iteration_dict):
        if self._total is None:
            self._total = 0
        self._total += iteration_dict['brain'].actual_time

    @memoize
    def total(self):
        if self._total is None:
            # projectlist hasn't been called yet, so do it to
            # update the total.
            self.projectlist()
        if self._total is None:
            # total could still be none if there are no iterations.
            return ''
        return formatTime(self._total)

    def sort_results(self, results):

        def sort_key(item):
            return item['completion_date']

        results.sort(key=sort_key)
        return results


class PlannedIterationsView(IterationListBaseView):

    iteration_review_state = ['new']

    def add_to_total(self, iteration_dict):
        if self._total is None:
            self._total = 0
        self._total += float(iteration_dict['rough_estimate'])

    @memoize
    def total(self):
        if self._total is None:
            # projectlist hasn't been called yet, so do it to
            # update the total.
            list(self.projectlist())
        if self._total is None:
            # total could still be none if there are no iterations.
            return ''
        return '%.2f' % self._total

    def extra_dict(self, obj, brain):
        """Add additional information to the iterationdict."""
        filter = dict(portal_type='Story')
        items = obj.getFolderContents(filter)
        rough_estimate = sum([item.size_estimate for item in items
                              if item.size_estimate is not None])
        return {'rough_estimate': '%.2f' % rough_estimate}

    def sort_results(self, results):

        def sort_key(item):
            return item['start_date']

        results.sort(key=sort_key)
        return results

    @memoize
    def project_url(self):
        return self.context.getProject().absolute_url()
