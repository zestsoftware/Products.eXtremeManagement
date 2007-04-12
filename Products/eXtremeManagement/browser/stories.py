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

        # Not all page templates are prepared for getting their data
        # as a dict, so just return the brains for now.
        # Affected are: story_view, iteration_view and task_overview
        # iteration_view uses a macro defined in story_view
        # task_overview uses a macro from iteraion_view
        return taskbrains        

        task_list = []

        for taskbrain in taskbrains:
            info = self.xt.taskbrain2dict(taskbrain)
            task_list.append(info)

        return task_list
