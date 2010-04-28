from webdav.Lockable import wl_isLocked
from Acquisition import aq_inner
from Acquisition import aq_parent
from Acquisition import Explicit
from zope.component import adapts
from zope.interface import Interface
from zope.publisher.interfaces.browser import IBrowserView
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.kss.plonekssview import PloneKSSView
from kss.core import kssaction
from Products.CMFCore.utils import getToolByName
from Products.eXtremeManagement.browser.xmbase import XMBaseView
from xm.booking.timing.interfaces import IActualHours
from xm.booking.timing.interfaces import IEstimate
from Products.eXtremeManagement.content.Iteration import \
    UNACCEPTABLE_STATUSES as UNACCEPTABLE_STORY_STATUSES
from Products.eXtremeManagement.utils import formatTime
from Products.eXtremeManagement.utils import getStateSortedContents
from Products.eXtremeManagement import XMMessageFactory as _


class IterationView(XMBaseView):
    """Simply return info about a Iteration.
    """

    def main(self):
        """Get a dict with info from this Context.
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

        # Size estimate.  We may want to do this smarter.
        filter = dict(portal_type='Story')
        items = context.getFolderContents(filter)
        size_estimate = sum([item.size_estimate for item in items
                             if item.size_estimate is not None])

        review_state = self.workflow.getInfoFor(context, 'review_state')
        if review_state in ['completed', 'invoiced', 'own-account']:
            budget_left = None
        else:
            budget_left = self.actual_budget_left()
        if budget_left is not None:
            budget_left = formatTime(budget_left)
        ploneview = context.restrictedTraverse('@@plone')
        if hasattr(context, 'getManHours'):
            manhours = context.getManHours()
        else:
            manhours = None
        returnvalue = dict(
            title = context.Title(),
            description = context.Description(),
            man_hours = manhours,
            start_date = ploneview.toLocalizedTime(context.getStartDate()),
            end_date = ploneview.toLocalizedTime(context.getEndDate()),
            estimate = formatTime(estimate),
            size_estimate = size_estimate,
            actual = formatTime(actual),
            difference = formatTime(estimate - actual),
            review_state = review_state,
            budget_left = budget_left,
            )
        return returnvalue

    def stories(self, sort_by_state=True, locked_status=False):
        context = aq_inner(self.context)
        filter = dict(portal_type='Story',
                      sort_on='getObjPositionInParent')
        storybrains = context.getFolderContents(filter)
        if sort_by_state:
            storybrains = getStateSortedContents(storybrains)

        story_list = []

        for storybrain in storybrains:
            info = self.storybrain2dict(storybrain, locked_status)
            story_list.append(info)

        return story_list

    def storybrain2dict(self, brain, locked_status=False):
        """Get a dict with info from this story brain.
        """
        context = aq_inner(self.context)
        review_state_id = brain.review_state

        # compute progress percentage
        is_completed = (review_state_id == 'completed')
        if is_completed:
            progress = 100
        else:
            estimated = brain.estimate
            actual = brain.actual_time
            progress = self.get_progress_perc(actual, estimated)

        # Extract locked status if requested
        locked = False
        if locked_status:
            locked = wl_isLocked(brain.getObject())

        # compute open task count
        searchpath = brain.getPath()
        filter = dict(portal_type=['Task', 'PoiTask'],
                      path=searchpath)
        unfinished_states = ('open', 'to-do', )
        filter['review_state'] = unfinished_states
        open_tasks = len(self.catalog.searchResults(**filter))

        # compute completed task count
        finished_states = ('completed', )
        filter['review_state'] = finished_states
        completed_tasks = len(self.catalog.searchResults(**filter))

        estimate = brain.estimate
        actual = brain.actual_time
        returnvalue = dict(
            story_id = brain.getId,
            uid = brain.UID,
            url = brain.getURL(),
            title = brain.Title,
            description = brain.Description,
            raw_estimate = estimate,
            estimate = formatTime(estimate),
            size_estimate = brain.size_estimate,
            actual = formatTime(actual),
            difference = formatTime(estimate - actual),
            progress = progress,
            review_state = review_state_id,
            review_state_title = self.workflow.getTitleForStateOnType(
                                 review_state_id, 'Story'),
            is_completed = is_completed,
            open_tasks = open_tasks,
            completed_tasks = completed_tasks,
            locked = locked,
        )
        return returnvalue

    def story_titles_not_startable(self):
        context = aq_inner(self.context)

        filter = dict(portal_type='Story',
                      sort_on='getObjPositionInParent')
        items = context.getFolderContents(filter)

        stories = [x.Title
                   for x in items
                   if x.review_state in UNACCEPTABLE_STORY_STATUSES]
        return ', '.join(stories)

    def get_progress_perc(self, part, total):
        """Get progress percentage of part compared to total.

        Set up some test context.

        >>> from zope.publisher.browser import TestRequest
        >>> class SimpleContext(object):
        ...     portal_properties = None
        >>> context = SimpleContext()
        >>> request = TestRequest()
        >>> view = IterationView(context, request)

        Test a part that is larger than the total:

        >>> view.get_progress_perc(3, 1)
        300

        We do not want to go over 100 percent though, so we have a
        setting in a property sheet that we use.  Set up a test
        environment for that.

        >>> xm_properties = dict(maximum_not_completed_percentage = 90)
        >>> portal_properties = dict()
        >>> portal_properties['xm_properties'] = xm_properties
        >>> view.context.portal_properties = portal_properties

        Now try again.

        >>> view.get_progress_perc(3, 1)
        90

        Code that uses this method can choose to show 100 percent to
        the user, for instance because a Story has the status
        'completed'.  But that is not our responsibility.

        Now for some more tests.

        >>> view.get_progress_perc(0, 1)
        0
        >>> view.get_progress_perc(10, 100)
        10
        >>> view.get_progress_perc(1, 3)
        33
        >>> view.get_progress_perc(1, 3.0)
        33

        """
        context = self.context
        if total > 0:
            try:
                percentage = int(round(part/float(total)*100))
            except TypeError:
                return '??'
            portal_properties = getToolByName(context, 'portal_properties',
                                              None)
            if portal_properties is None:
                return percentage
            xm_props = portal_properties.get('xm_properties', None)
            if xm_props is None:
                return percentage
            max_percentage = xm_props.get('maximum_not_completed_percentage',
                                          90.0)
            if percentage > max_percentage:
                return max_percentage
            return percentage
        return 0

    def actual_budget_left(self):
        context = self.context
        project = aq_parent(aq_inner(self.context))
        hours_left = project.getBudgetHours()
        if not hours_left:
            return None
        contentfilter = dict(portal_type = 'Iteration')
        iteration_brains = project.getFolderContents(contentfilter)
        for brain in iteration_brains:
            iteration = brain.getObject()
            hours_left -= IActualHours(brain.getObject()).actual_time
        return hours_left

    def second_current_iteration(self):
        """Link to the other iteration that is in state in-progress"""
        project = aq_parent(aq_inner(self.context))
        contentfilter = dict(portal_type = 'Iteration',
                             review_state = 'in-progress')
        brains = project.getFolderContents(contentfilter)
        # If we have multiple iterations in progress this return a link to it
        # In the template we will display a statusmessage.
        if len(brains) >= 2:
            if self.context.getId() == brains[0].getId:
                return brains[1].getURL()
            elif self.context.getId() == brains[1].getId:
                return brains[0].getURL()
        return False


class PlanningView(IterationView):
    """
    An alternate view for iterations that allows quick estimation of stories
    """

    def update(self):
        form = self.request.form
        submitted = form.get('form.submitted', False)
        if submitted:
            for story in self.stories():
                new_val = self.request.get(str(story['uid']))
                if new_val:
                    story_obj = self.context.get(story['story_id'])
                    story_obj.set_size_estimate(float(new_val))


class IterationForm(Explicit):
    adapts(Interface, IDefaultBrowserLayer, IBrowserView)

    def update(self):
        pass

    render = ViewPageTemplateFile("add_iteration.pt")


class IterationList(Explicit):
    adapts(Interface, IDefaultBrowserLayer, IBrowserView)

    def __init__(self, context, request, view):
        self.__parent__ = view
        self.context = context
        self.request = request
        self.view = view
        planned = self.context.restrictedTraverse('@@planned-iterations')
        self.projectlist = planned.projectlist()
        self.total = planned.total()

    def update(self):
        pass


    render = ViewPageTemplateFile("iteration_list.pt")


class Create(BrowserView):
    """Create a new iteration"""

    def __call__(self):
        form = self.request.form
        title = form.get('title', '')
        if title == '':
            #status message
            return
        context = aq_inner(self.context)
        plone_utils = getToolByName(self.context, 'plone_utils')
        new_id = plone_utils.normalizeString(title)
        context.invokeFactory(type_name="Iteration", id=new_id, title=title)
        plone_utils.addPortalMessage(_(u'Iteration added.'))
        self.request.response.redirect(context.absolute_url() + '/@@planned-iterations')


class Add(PloneKSSView):

    @kssaction
    def add_iteration(self):
        context = aq_inner(self.context)
        plone_commands = self.getCommandSet('plone')
        title = self.request.form.get('title')
        if not title:
            plone_commands.issuePortalMessage(_(u'Title is required'),
                                              msgtype='error')
            return None
        plone_utils = getToolByName(self.context, 'plone_utils')
        new_id = plone_utils.normalizeString(title)
        context.invokeFactory(type_name="Iteration", id=new_id, title=title)
        core = self.getCommandSet('core')
        zopecommands = self.getCommandSet('zope')
        zopecommands.refreshProvider('#iterationlist', name = 'xm.iteration_list')
        zopecommands.refreshProvider('#add-iteration', name = 'xm.iteration_form')
        plone_commands.issuePortalMessage(_(u'Iteration added.'),
                                          msgtype='info')
