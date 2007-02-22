from zope.interface import Interface


class IXMTask(Interface):
    """eXtremeManagement Task

    A Task is a subset of a Story.  It can be assigned to one or more
    employees.  A Task should not take more than one day.

    A Task contains Bookings.
    """
