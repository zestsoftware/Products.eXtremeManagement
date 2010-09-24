from zope.app.publisher.interfaces.browser import IBrowserMenu
from zope.component import getUtility
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent


def createBooking(container, id=id, hours=0, minutes=0):
    """Create a Booking and fire the ObjectModifiedEvent.

    The event is fired automatically for you when you press Save in
    the edit form, but in testing we apparently need to take care of
    it ourselves.
    """
    container.invokeFactory('Booking', id=id)
    booking = container[id]
    booking.update(hours=hours, minutes=minutes)
    notify(ObjectModifiedEvent(booking))


def list_addable(context):
    menu = getUtility(IBrowserMenu, name='plone_contentmenu_factory',
                      context=context)
    menu_items = menu.getMenuItems(context, context.REQUEST)
    return u', '.join([m.get('title') for m in menu_items])
