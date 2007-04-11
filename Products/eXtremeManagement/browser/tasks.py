from Products.CMFCore.utils import getToolByName

class SimpleTaskView(object):
    """Simply return info about a Task.
    """

    def __init__(self, context, request=None):
        self.context = context
        self.catalog = getToolByName(self.context, 'portal_catalog')
        self.workflow = getToolByName(self.context, 'portal_workflow')
        self.xt = getToolByName(self.context, 'xm_tool')
        if request is None:
            # At least handy for testing.
            self.request = self.context.REQUEST
        else:
            self.request = request
 
    def task2dict(self):
        """Get a dict with info from this Task.
        """
        task = self.context
        returnvalue = dict(
            title = task.Title(),
            description = task.Description(),
            cooked_body = task.CookedBody(),
            estimate = self.xt.formatTime(task.getRawEstimate()),
            actual = self.xt.formatTime(task.getRawActualHours()),
            difference = self.xt.formatTime(task.getRawDifference()),
            review_state = self.workflow.getInfoFor(task, 'review_state'),
            assignees = task.getAssignees(),
            )
        return returnvalue
