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


class IXMBaseView(Interface):
    """Info about one of the standard content types of
    eXtremeManagement.
    """

    def main():
        """Get a dict with info from this object.
        """


class ITaskView(IXMBaseView):
    """Info about a task
    """

    def main():
        """Get a dict with info from this object.
        """


class IStoryView(IXMBaseView):
    """Info about a story
    """

    def main():
        """Get a dict with info from this object.
        """


class IIterationView(IXMBaseView):
    """Info about a iteration
    """

    def main():
        """Get a dict with info from this object.
        """
