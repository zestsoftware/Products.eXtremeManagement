from Products.Five.browser import BrowserView
from Acquisition import aq_inner


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
