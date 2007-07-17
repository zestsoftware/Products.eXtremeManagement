from Products.Five.browser import BrowserView
from Acquisition import aq_inner


class XMBaseView(BrowserView):
    """Base view for showing info about an object.
    """

    def __init__(self, context, request):
        super(XMBaseView, self).__init__(context, request)
        context = aq_inner(context)
 
    def main(self):
        """Get a dict with info from this object.
        """
        return {}
