from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView


class XMBaseView(BrowserView):
    """Base view for showing info about an object.
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.xt = getToolByName(self.context, 'xm_tool')
 
    def main(self):
        """Get a dict with info from this object.
        """
        return {}
