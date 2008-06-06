from Acquisition import aq_inner
from zope.component import adapter
from kss.core.interfaces import IKSSView
from Products.DCWorkflow.interfaces import IAfterTransitionEvent
#from plone.app.kss.plonekssview import PloneKSSView
from Products.eXtremeManagement.interfaces.xmstory import IXMStory

@adapter(IXMStory, IKSSView, IAfterTransitionEvent)
def workflow_changed(obj, view, event):
    if not (event.old_state is event.new_state):
        #obj.reindexObject()
        viewletReloader = ViewletReloader(view)
        viewletReloader.xm_change_workflow_state()


class ViewletReloader(object):
    """Reload xm viewlets that depend on the workflow state.
    """

    def __init__(self, view):
        self.view = view
        self.context = view.context
        self.request = view.request

    def xm_change_workflow_state(self):
        """Refresh some viewlets.
        """
        zope = self.view.getCommandSet('zope')
        zope.refreshProvider('#task-list-for-story',
                             'xm.tasklist.simple')
        zope.refreshViewlet('#add-task', 'plone.belowcontentbody',
                            'xm.add_task_form')
