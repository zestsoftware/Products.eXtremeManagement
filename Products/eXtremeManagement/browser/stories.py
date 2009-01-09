from Acquisition import aq_inner
from Acquisition import aq_parent
from kss.core import kssaction
from plone.app.kss.plonekssview import PloneKSSView

from Products.eXtremeManagement.browser.xmbase import XMBaseView
from Products.eXtremeManagement.utils import formatTime
from xm.booking.timing.interfaces import IActualHours
from xm.booking.timing.interfaces import IEstimate


class StoryView(XMBaseView):
    """Simply return info about a Story.
    """

    def main(self):
        """Get a dict with info from this Story.
        """
        context = aq_inner(self.context)

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
            review_state = self.workflow.getInfoFor(context, 'review_state'),
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
        mtool = self.tools().membership()
        currentUser = mtool.getAuthenticatedMember().getId()
        # all the member that work on this project
        # XXX test if user folders somewhere else are recognized too
        employees = self.context.getProject().getMembers(role='Employee')
        assignables = []
        # build result
        for mId in employees:
            member = mtool.getMemberById(mId)
            if member is not None:
                fullname = member.getProperty('fullname', None)
                # if fullname is '' or None, return the id
                name = fullname and fullname.strip() or mId
            else:
                name = mId
            assignables.append(dict(id = mId, name = name))
        return assignables


class StoryToggle(PloneKSSView):
    """KSS for toggling the display of a story.
    """

    @kssaction
    def xm_toggle_story(self, uid):
        """Toggle the display of the story with the given uid.
        """
        # Render the story details provider for this story
        zope = self.getCommandSet('zope')
        zope.refreshProvider('#story-details-target-' + uid,
                             'xm.story.details')

        # Toggle the display of the story details by toggling the
        # class.
        core = self.getCommandSet('core')
        core.toggleClass('#story-details-' + uid, 'story-details-empty')

        # Toggle the display of the bottom line of the main story row.
        core.toggleClass('#story-title-' + uid, 'clear-bottom')
