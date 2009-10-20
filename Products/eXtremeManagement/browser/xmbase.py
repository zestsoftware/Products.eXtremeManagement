from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from zope.cachedescriptors.property import Lazy
from zope.component import getMultiAdapter

class XMBaseView(BrowserView):
    """Base view for showing info about an object.
    """
    # request and context should be set on class level to prevent this
    # WARNING on startup (Plone 3.0):
    # Init Class Products.Five.metaclass.ProjectView has a security
    # declaration for nonexistent method 'request' (or 'context')
    request = None
    context = None

    def main(self):
        """Get a dict with info from this object.
        """
        return {}

    @Lazy
    def workflow(self):
        context = aq_inner(self.context)
        return getToolByName(context, 'portal_workflow')

    @Lazy
    def catalog(self):
        context = aq_inner(self.context)
        return getToolByName(context, 'portal_catalog')

    def tools(self):
        return getMultiAdapter((self.context, self.request),
                                name=u'plone_tools')

    @property
    def portal_state(self):
        return getMultiAdapter((self.context, self.request),
                                name=u'plone_portal_state')
