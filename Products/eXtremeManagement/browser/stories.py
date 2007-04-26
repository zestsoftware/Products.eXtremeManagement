from Products.CMFCore.utils import getToolByName
from Products.eXtremeManagement.browser.xmbase import XMBaseView
from Acquisition import aq_inner


class StoryView(XMBaseView):
    """Simply return info about a Story.
    """

    def main(self):
        """Get a dict with info from this Story.
        """
        context = aq_inner(self.context)
        workflow = getToolByName(context, 'portal_workflow')
        returnvalue = dict(
            title = context.Title(),
            description = context.Description(),
            cooked_body = context.CookedBody(),
            rough_estimate = context.getRoughEstimate(),
            review_state = workflow.getInfoFor(context, 'review_state'),
            )
        return returnvalue

    def totals(self):
        """Get a dict with totals for this Story.
        """
        context = aq_inner(self.context)
        totals = dict(
            estimate = self.xt.formatTime(context.getRawEstimate()),
            actual = self.xt.formatTime(context.getRawActualHours()),
            difference = self.xt.formatTime(context.getRawDifference()),
            )
        return totals

    def tasks(self):
        context = aq_inner(self.context)
        view = context.restrictedTraverse('@@task_details')
        return view.tasklist()

    def taskbrain2dict(self, brain):
        """Get a dict with info from this task brain.
        """
        context = aq_inner(self.context)
        review_state_id = brain.review_state
        workflow = getToolByName(context, 'portal_workflow')
        returnvalue = dict(
            url = brain.getURL(),
            title = brain.Title,
            description = brain.Description,
            estimate = self.xt.formatTime(brain.getRawEstimate),
            actual = self.xt.formatTime(brain.getRawActualHours),
            difference = self.xt.formatTime(brain.getRawDifference),
            review_state = review_state_id,
            review_state_title = workflow.getTitleForStateOnType(
                                 review_state_id, 'Task'),
            assignees = brain.getAssignees,
        )
        return returnvalue
