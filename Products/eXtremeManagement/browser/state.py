import Acquisition
from Products.Five import BrowserView
from zope.cachedescriptors.property import Lazy
from plone.memoize.view import memoize_contextless

from Products.eXtremeManagement.browser.xmbase import XMBaseView
from Products.eXtremeManagement import interfaces


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

    @Lazy
    def project(self):
        context = Acquisition.aq_inner(self.context)
        if interfaces.IXMProject.providedBy(context):
            return context

        iteration = self.iteration
        if iteration is None:
            return None
        return Acquisition.aq_parent(iteration)

    @Lazy
    def iteration(self):
        context = Acquisition.aq_inner(self.context)
        if interfaces.IXMIteration.providedBy(context):
            return context

        story = self.story
        if story is None:
            return None
        return Acquisition.aq_parent(story)

    @Lazy
    def story(self):
        context = Acquisition.aq_inner(self.context)
        if interfaces.IXMStory.providedBy(context):
            return context
        if interfaces.IXMTask.providedBy(context):
            return Acquisition.aq_parent(context)
        return None


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
