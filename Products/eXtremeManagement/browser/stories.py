from Products.CMFCore.utils import getToolByName

class SimpleStoryView(object):
    """Simply return info about a Story.
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
 
    def story2dict(self):
        """Get a dict with info from this Story.
        """
        story = self.context
        returnvalue = dict(
            title = story.Title(),
            description = story.Description(),
            cooked_body = story.CookedBody(),
            estimate = self.xt.formatTime(story.getRawEstimate()),
            actual = self.xt.formatTime(story.getRawActualHours()),
            difference = self.xt.formatTime(story.getRawDifference()),
            rough_estimate = story.getRoughEstimate(),
            review_state = self.workflow.getInfoFor(story, 'review_state'),
            )
        return returnvalue
