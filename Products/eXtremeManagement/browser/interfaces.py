from zope.interface import Interface

class IMyProjects(Interface):
    """Return the projects that the logged in user has tasks in.
    """

    def projectlist():
        pass


class IBookingListView(Interface):
    """Return list of bookings
    """

    def bookinglist():
        pass


class ITaskView(Interface):
    """Info about a task
    """

    def main():
        pass


class IStoryView(Interface):
    """Info about a story
    """

    def main():
        pass


class IIterationView(Interface):
    """Info about a iteration
    """

    def main():
        pass
