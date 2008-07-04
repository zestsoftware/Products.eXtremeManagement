from zope.component import adapter
from kss.core.interfaces import IKSSView
from Products.DCWorkflow.interfaces import IAfterTransitionEvent

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
        if IXMStory.providedBy(self.context):
            # only do this if the context is actually a Story.
            zope = self.view.getCommandSet('zope')
            zope.refreshProvider('#task-list-for-story',
                                 'xm.tasklist.simple')
            zope.refreshViewlet('#add-task', 'plone.belowcontentbody',
                                'xm.add_task_form')

    def update_task_viewlets(self):
        """Refresh task viewlets.
        """
        if IXMTask.providedBy(self.context):
            # only do this if the context is actually a task.
            zope = self.view.getCommandSet('zope')
            zope.refreshViewlet('#add-booking', 'plone.belowcontentbody',
                                'xm.add_booking_form')
