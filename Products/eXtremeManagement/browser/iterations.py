from Products.CMFCore.utils import getToolByName
from Products.eXtremeManagement.browser.xmbase import XMBaseView


class IterationView(XMBaseView):
    """Simply return info about a Iteration.
    """

    def main(self):
        """Get a dict with info from this Iteration.
        """
        iteration = self.context
        return self.xt.iteration2dict(iteration)

    def stories(self):
        current_path = '/'.join(self.context.getPhysicalPath())
        storybrains = self.xt.getStateSortedContents(self.context)
        story_list = []

        for storybrain in storybrains:
            info = self.xt.storybrain2dict(storybrain)
            story_list.append(info)

        return story_list
