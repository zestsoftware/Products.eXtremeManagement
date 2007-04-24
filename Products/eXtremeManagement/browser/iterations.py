from Products.CMFCore.utils import getToolByName
from Products.eXtremeManagement.browser.xmbase import XMBaseView


class IterationView(XMBaseView):
    """Simply return info about a Iteration.
    """

    def main(self):
        """Get a dict with info from this Context.
        """
        context = self.context
        workflow = getToolByName(context, 'portal_workflow')
        returnvalue = dict(
            title = context.Title(),
            description = context.Description(),
            man_hours = context.getManHours(),
            start_date = context.restrictedTraverse('@@plone').toLocalizedTime(context.getStartDate()),
            end_date = context.restrictedTraverse('@@plone').toLocalizedTime(context.getEndDate()),
            estimate = self.xt.formatTime(context.getRawEstimate()),
            actual = self.xt.formatTime(context.getRawActualHours()),
            difference = self.xt.formatTime(context.getRawDifference()),
            review_state = workflow.getInfoFor(context, 'review_state'),
            )
        return returnvalue

    def stories(self):
        current_path = '/'.join(self.context.getPhysicalPath())
        storybrains = self.xt.getStateSortedContents(self.context)
        story_list = []

        for storybrain in storybrains:
            info = self.storybrain2dict(storybrain)
            story_list.append(info)

        return story_list

    def storybrain2dict(self, brain):
        """Get a dict with info from this story brain.
        """
        context = self.context
        review_state_id = brain.review_state
        workflow = getToolByName(context, 'portal_workflow')
        catalog = getToolByName(context, 'portal_catalog')

        # compute progress percentage
        if review_state_id == 'completed':
            progress = 100
        else:
            estimated = brain.getRawEstimate
            actual = brain.getRawActualHours
            progress = self.xt.get_progress_perc(actual, estimated)

        # compute open task count
        searchpath = brain.getPath()
        filter = dict(portal_type='Task',
                      path=searchpath)
        unfinished_states = ('open','to-do',)
        filter['review_state'] = unfinished_states
        open_tasks = len(catalog.searchResults(**filter))

        # compute completed task count
        finished_states = ('completed',)
        filter['review_state'] = finished_states
        completed_tasks = len(catalog.searchResults(**filter))

        returnvalue = dict(
            url = brain.getURL(),
            title = brain.Title,
            description = brain.Description,
            estimate = self.xt.formatTime(brain.getRawEstimate),
            actual = self.xt.formatTime(brain.getRawActualHours),
            difference = self.xt.formatTime(brain.getRawDifference),
            progress = progress,
            review_state = review_state_id,
            review_state_title = workflow.getTitleForStateOnType(
                                 review_state_id, 'Story'),
            open_tasks = open_tasks,
            completed_tasks = completed_tasks,
        )
        return returnvalue

    
