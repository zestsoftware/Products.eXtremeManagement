from urlparse import urlsplit

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.DCWorkflow.interfaces import IAfterTransitionEvent
from kss.core import kssaction, KSSExplicitError
from kss.core.interfaces import IKSSView
from plone.app.kss.interfaces import IPloneKSSView
from plone.app.kss.plonekssview import PloneKSSView
from plone.app.layout.globals.interfaces import IViewView
from plone.locking.interfaces import ILockable
from zope.component import adapter
from zope.interface import implements

from Products.eXtremeManagement.interfaces import IXMStory
from Products.eXtremeManagement.interfaces import IXMTask


@adapter(IXMStory, IKSSView, IAfterTransitionEvent)
def story_workflow_changed(obj, view, event):
    if not (event.old_state == event.new_state):
        viewletReloader = ViewletReloader(view)
        viewletReloader.update_story_viewlets()


@adapter(IXMTask, IKSSView, IAfterTransitionEvent)
def task_workflow_changed(obj, view, event):
    if not (event.old_state == event.new_state):
        viewletReloader = ViewletReloader(view)
        viewletReloader.update_task_viewlets()


class ViewletReloader(object):
    """Reload xm viewlets that depend on the workflow state.
    """

    def __init__(self, view):
        self.view = view
        self.context = view.context
        self.request = view.request

    def update_story_viewlets(self):
        """Refresh story viewlets.
        """
        context = aq_inner(self.context)
        if IXMStory.providedBy(context):
            # only do this if the context is actually a Story.
            zope = self.view.getCommandSet('zope')
            zope.refreshProvider('.tasklist_table',
                                 'xm.tasklist.simple')
            zope.refreshProvider('#add-task', 'xm.task_form')

            # Refresh the details box provider
            zope.refreshProvider('.xm-details',
                                 'xm.story.detailsbox')

    def update_task_viewlets(self):
        """Refresh task viewlets.
        """
        if IXMTask.providedBy(self.context):
            # only do this if the context is actually a task.
            zope = self.view.getCommandSet('zope')
            zope.refreshViewlet('#add-booking', 'plone.belowcontentbody',
                                'xm.add_booking_form')


class KSSTaskForm(PloneKSSView):

    @kssaction
    def kss_task_form(self):
        """Return the add task form"""
        core = self.getCommandSet('core')
        zope = self.getCommandSet('zope')
        selector = core.getHtmlIdSelector('task-form')
        zope.refreshProvider(selector, 'xm.task_form')


class KSSIterationForm(PloneKSSView):

    @kssaction
    def kss_iteration_form(self):
        """Return the add iteration form"""
        core = self.getCommandSet('core')
        zope = self.getCommandSet('zope')
        selector = core.getHtmlIdSelector('iteration-form')
        zope.refreshProvider(selector, 'xm.iteration_form')


class WorkflowGadget(PloneKSSView):

    implements(IPloneKSSView, IViewView)

    @kssaction
    def xmChangeWorkflowState(self, uid, url):
        """Change the workflow state, currently only of a Task."""
        context = aq_inner(self.context)
        ksscore = self.getCommandSet('core')
        zopecommands = self.getCommandSet('zope')
        plonecommands = self.getCommandSet('plone')

        locking = ILockable(context, None)
        if locking is not None and not locking.can_safely_unlock():
            selector = ksscore.getHtmlIdSelector('plone-lock-status')
            zopecommands.refreshViewlet(selector, 'plone.abovecontent',
                                        'plone.lockinfo')
            plonecommands.refreshContentMenu()
            return self.render()

        (proto, host, path, query, anchor) = urlsplit(url)
        if not path.endswith('content_status_modify'):
            raise KSSExplicitError('only content_status_modify is handled')
        action = query.split("workflow_action=")[-1].split('&')[0]
        uid_catalog = getToolByName(context, 'uid_catalog')
        brain = uid_catalog(UID=uid)[0]
        obj = brain.getObject()
        obj.content_status_modify(action)
        if IXMStory.providedBy(self.context):
            # Only refresh content if the context is a Story,
            # otherwise you get too much tasks listed.
            selector = ksscore.getCssSelector('.contentViews')
            zopecommands.refreshViewlet(selector, 'plone.contentviews',
                                        'plone.contentviews')
            zopecommands.refreshProvider('.tasklist_table',
                                         'xm.tasklist.simple')
            plonecommands.refreshContentMenu()
        else:
            # In all other cases, we can at least refresh the part
            # that shows the workflow info for this item.
            wf_change = obj.restrictedTraverse('xm_workflow_change')
            html = wf_change()
            selector = ksscore.getHtmlIdSelector('id-%s' % uid)
            ksscore.replaceHTML(selector, html)
        self.issueAllPortalMessages()
        self.cancelRedirect()
