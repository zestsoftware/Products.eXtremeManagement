from Products.CMFCore.utils import getToolByName
from Products.eXtremeManagement.browser.xmbase import XMBaseView


class StoryView(XMBaseView):
    """Simply return info about a Story.
    """

    def main(self):
        """Get a dict with info from this Story.
        """
        context = self.context
        workflow = getToolByName(context, 'portal_workflow')
        returnvalue = dict(
            title = context.Title(),
            description = context.Description(),
            cooked_body = context.CookedBody(),
            estimate = self.xt.formatTime(context.getRawEstimate()),
            actual = self.xt.formatTime(context.getRawActualHours()),
            difference = self.xt.formatTime(context.getRawDifference()),
            rough_estimate = context.getRoughEstimate(),
            review_state = workflow.getInfoFor(context, 'review_state'),
            )
        return returnvalue

    def tasks(self):
        current_path = '/'.join(self.context.getPhysicalPath())
        taskbrains = self.xt.getStateSortedContents(self.context)

        # Not all page templates are prepared for getting their data
        # as a dict, so just return the brains for now.
        # Affected are: story_view, iteration_view and task_overview
        # iteration_view uses a macro defined in story_view
        # task_overview uses a macro from iteraion_view
        return taskbrains        

        task_list = []

        for taskbrain in taskbrains:
            info = self.taskbrain2dict(taskbrain)
            task_list.append(info)

        return task_list

    def taskbrain2dict(self, brain):
        """Get a dict with info from this task brain.
        """
        context = self.context
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
