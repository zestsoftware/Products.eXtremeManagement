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
