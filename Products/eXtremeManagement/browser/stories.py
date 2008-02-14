from Acquisition import aq_inner
from Acquisition import aq_parent
from Products.CMFCore.utils import getToolByName

from Products.eXtremeManagement.browser.xmbase import XMBaseView
from xm.booking.timing.interfaces import IActualHours
from xm.booking.timing.interfaces import IEstimate
from Products.eXtremeManagement.utils import formatTime


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
            estimate = formatTime(estimate),
            actual = formatTime(actual),
            difference = formatTime(estimate - actual),
            )
        return totals

    def tasklist(self):
        context = aq_inner(self.context)
        view = context.restrictedTraverse('@@task_details')
        return view.tasklist(sort_by_state=True)

    def task_titles_not_startable(self):
        tasks = [x.title_or_id()
                 for x in self.context.getStoryTasks()
                 if not x.startable()]
        return ', '.join(tasks)

    def show_add_task_form(self):
        addable = [t.Metatype() for t in self.context.allowedContentTypes()]
        return 'Task' in addable

    def get_possible_assignees(self):
        mtool = getToolByName(self, 'portal_membership')
        currentUser = mtool.getAuthenticatedMember().getId()
        # all the member that work on this project
        # XXX test if user folders somewhere else are recognized too
        employees = self.context.getProject().getMembers(role='Employee')
        assignables = []
        # build result
        for memberId in employees:
            if memberId == currentUser:
                default = 'selected'
            else:
                default = ''
            member = mtool.getMemberById(memberId)
            if member is not None:
                fullname = member.getProperty('fullname', None)
                # if fullname is '' or None, return the id
                name = fullname and fullname.strip() or member.getId()
            else:
                name = memberId
            assignables.append((memberId, name, default))
        return assignables
