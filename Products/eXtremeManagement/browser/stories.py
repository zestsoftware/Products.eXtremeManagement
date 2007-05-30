from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName

from Products.eXtremeManagement.browser.xmbase import XMBaseView
from Acquisition import aq_inner, aq_parent
from Products.eXtremeManagement.timing.interfaces import IActualHours
from Products.eXtremeManagement.timing.interfaces import IEstimate


class StoryView(XMBaseView):
    """Simply return info about a Story.
    """

    def main(self):
        """Get a dict with info from this Story.
        """
        context = aq_inner(self.context)
        workflow = getToolByName(context, 'portal_workflow')

        # get info for previous and next links
        iteration = aq_parent(context)
        stories = iteration.getFolderContents()
        num_stories = len(stories)
        pos = iteration.getObjectPosition(context.id)
        next = pos < num_stories-1 and stories[pos+1]
        prev = pos != 0 and stories[pos-1]

        returnvalue = dict(
            title = context.Title(),
            description = context.Description(),
            cooked_body = context.CookedBody(),
            rough_estimate = context.getRoughEstimate(),
            review_state = workflow.getInfoFor(context, 'review_state'),
            prev = prev,
            next = next,
            )
        return returnvalue

    def totals(self):
        """Get a dict with totals for this Story.
        """
        context = aq_inner(self.context)
        anno = IActualHours(context, None)
        if anno is not None:
            actual = anno.actual_time
        else:
            # Should not happen (tm).
            actual = -99.0
        est = IEstimate(context, None)
        if est is not None:
            estimate = est.estimate
        else:
            # Should not happen (tm).
            estimate = -99.0
        totals = dict(
            estimate = self.xt.formatTime(estimate),
            actual = self.xt.formatTime(actual),
            difference = self.xt.formatTime(estimate - actual),
            )
        return totals

    def tasks(self):
        context = aq_inner(self.context)
        view = context.restrictedTraverse('@@task_details')
        return view.tasklist(sort_by_state=True)
