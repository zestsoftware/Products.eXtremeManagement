from Products.CMFCore.utils import getToolByName
from Products.eXtremeManagement.browser.xmbase import XMBaseView


class IterationView(XMBaseView):
    """Simply return info about a Iteration.
    """

    def main(self):
        """Get a dict with info from this Iteration.
        """
        iteration = self.context
        return self.xt.iteration2dict(iteration)
