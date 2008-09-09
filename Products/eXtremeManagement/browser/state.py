from Products.Five import BrowserView
from zope.cachedescriptors.property import Lazy
from plone.memoize.view import memoize_contextless

from Products.eXtremeManagement.browser.xmbase import XMBaseView


class XMGlobalState(BrowserView):
    """Global information about eXtremeManagement.

    Global here means: it is the same for all contexts.
    """

    @memoize_contextless
    def has_tracker(self):
        try:
            import xm.tracker
        except ImportError:
            return False
        return True


class WorkflowChangeView(XMBaseView):

    @Lazy
    def transitions(self):
        return self.workflow.getTransitionsFor(self.context)

    @Lazy
    def review_state_id(self):
        return self.workflow.getInfoFor(self.context, 'review_state')

    @Lazy
    def review_state_title(self):
        return self.workflow.getTitleForStateOnType(
            self.review_state_id, self.context.portal_type)
