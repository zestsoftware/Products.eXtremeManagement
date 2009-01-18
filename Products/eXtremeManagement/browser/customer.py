from Products.eXtremeManagement.browser.management import IterationListBaseView
from Products.eXtremeManagement.utils import formatTime


class FinishedIterationsView(IterationListBaseView):

    iteration_review_state = ['completed', 'invoiced']    

    def add_to_total(self, iteration_dict):
        if self._total is None:
            self._total = 0
        self._total += iteration_dict['brain'].actual_time

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
        
    def project_url(self):
        return self.context.getProject().absolute_url()
