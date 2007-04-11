from zope.interface import Interface

class IMyProjects(Interface):
    """Return the projects that the logged in user has tasks in.
    """

    def projectlist():
        pass


class IBookingView(Interface):
    """Return bookings
    """

    def bookinglist():
        pass


class ITaskView(Interface):
    """Return a task
    """

    def task2dict():
        pass
