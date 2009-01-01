from Products.eXtremeManagement.browser.management import IterationListBaseView


class FinishedIterationsView(IterationListBaseView):

    iteration_review_state = ['completed', 'invoiced']
    # sort on date completed
