from zope.interface import Interface


class IXMBooking(Interface):
    """eXtremeManagement Booking

    A Booking is made by an employee to show that he did some work on
    a Task.  Add all Bookings and you know how long the Task (and its
    parent Story and parent Iteration) actually took.  This can be
    used to bill the customer.

    A Booking contains no other content types.  Next to ProjectMember
    it is the only non-folderish content type we define.
    """
