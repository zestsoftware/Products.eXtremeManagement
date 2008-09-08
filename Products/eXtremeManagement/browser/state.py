from Products.Five import BrowserView
from plone.memoize.view import memoize, memoize_contextless


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


