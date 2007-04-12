from Products.CMFCore.utils import getToolByName
from Products.eXtremeManagement.browser.xmbase import XMBaseView


class TaskView(XMBaseView):
    """Simply return info about a Task.
    """
 
    def main(self):
        """Get a dict with info from this Task.
        """
        task = self.context
        return self.xt.task2dict(task)

    def bookings(self):
        current_path = '/'.join(self.context.getPhysicalPath())
        catalog = getToolByName(self.context, 'portal_catalog')
        bookings = [brain.getObject() for brain in
                    catalog.searchResults(portal_type='Booking',
                                          sort_on='getBookingDate',
                                          path=current_path)]
        return bookings
