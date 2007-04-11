from Products.CMFCore.utils import getToolByName

class TaskView(object):
    """Simply return info about a Task.
    """

    def __init__(self, context, request=None):
        self.context = context
        self.xt = getToolByName(self.context, 'xm_tool')
        if request is None:
            # At least handy for testing.
            self.request = self.context.REQUEST
        else:
            self.request = request
 
    def main(self):
        """Get a dict with info from this Task.
        """
        task = self.context
        return self.xt.task2dict(task)
