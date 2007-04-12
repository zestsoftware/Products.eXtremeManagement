from Products.CMFCore.utils import getToolByName
from Products.eXtremeManagement.browser.xmbase import XMBaseView


class StoryView(XMBaseView):
    """Simply return info about a Story.
    """

    def main(self):
        """Get a dict with info from this Story.
        """
        story = self.context
        return self.xt.story2dict(story)

    def tasks(self):
        current_path = '/'.join(self.context.getPhysicalPath())
        taskbrains = self.xt.getStateSortedContents(self.context)
        task_list = []

        for taskbrain in taskbrains:
            info = self.xt.taskbrain2dict(taskbrain)
            task_list.append(info)

        return task_list
