from Products.eXtremeManagement.browser.management import IterationListBaseView


class FinishedIterationsView(IterationListBaseView):

    iteration_review_state = ['completed', 'invoiced']

    def sort_results(self, results):

        def sort_key(item):
            return item['completion_date']

        results.sort(key=sort_key)
        return results


class PlannedIterationsView(IterationListBaseView):

    iteration_review_state = ['new']

    def sort_results(self, results):

        def sort_key(item):
            return item['start_date']

        results.sort(key=sort_key)
        return results