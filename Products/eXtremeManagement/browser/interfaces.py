from zope.interface import Interface, Attribute

class IMyProjects(Interface):
    """Return the projects that the logged in user has tasks in.
    """

    def projectlist():
        pass


class IBookingsDetailedView(Interface):
    """Return list of bookings
    """

    bookinglist = Attribute("List of individual Bookings")

    def main():
        """Get a dict with the main info, including total.
        """


class IBookingOverview(Interface):
    """Return overview of bookings for this period
    """

    bookinglist = Attribute("List of individual Bookings")

    def main():
        """Get a dict with the main info, including total.
        """


class IYearBookingOverview(Interface):
    """Return overview of bookings for a year, grouped by month.
    """

    def main():
        """Get a dict with the main info.
        """

    def months_list():
        """List with info about the past twelve months
        """
    

class IDayBookingOverview(Interface):
    """Return overview of bookings for a day
    """

    raw_total =  Attribute("Raw total booked hours for this day")
    total =  Attribute("Formatted total booked hours for this day")


class IXMBaseView(Interface):
    """Info about one of the standard content types of
    eXtremeManagement.
    """

    def main():
        """Get a dict with info from this object.
        """


class IBookingView(IXMBaseView):
    """Info about a booking
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

    def bookings():
        """Return the Bookings of this Task,  sorted by bookingDate
        """

class IStoryView(IXMBaseView):
    """Info about a story
    """

    def main():
        """Get a dict with info from this object.
        """

    def tasks():
        """Return the Tasks of this Story
        """


class IIterationView(IXMBaseView):
    """Info about a iteration
    """

    def main():
        """Get a dict with info from this object.
        """

    def stories():
        """Return the Stories of this Iteration
        """

class IProjectView(IXMBaseView):
    """Info about a project
    """

    def main():
        """Get a dict with info from this object.
        """
