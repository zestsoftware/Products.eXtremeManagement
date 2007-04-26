from zope.interface import Attribute
from zope.app.publisher.interfaces.browser import IBrowserView


class IMyProjects(IBrowserView):
    """Return the projects that the logged in user has tasks in.
    """

    def projectlist():
        pass


class IBookingsDetailedView(IBrowserView):
    """Return list of bookings
    """

    bookinglist = Attribute("List of individual Bookings")

    def main():
        """Get a dict with the main info, including total.
        """


class ITasksDetailedView(IBrowserView):
    """Return list of everyone's Tasks in all states
    """

    def tasklist():
        """List of all tasks in this context with totals
        """

    def simple_tasklist():
        """List of all tasks (brains) in this context
        """


class IMyTasksDetailedView(ITasksDetailedView):
    """Return list of my Tasks, in a particular state
    """

    state = Attribute("Review state to show")

    possible_states = Attribute("Other possible states")

    def projects():
        """List of projects in this context, with task info included.
        """

    def tasklist():
        """List of all tasks in this context with totals
        """

    def simple_tasklist():
        """List of all tasks (brains) in this context
        """


class IBookingOverview(IBrowserView):
    """Return overview of bookings for this period
    """

    bookinglist = Attribute("List of individual Bookings")

    def main():
        """Get a dict with the main info, including total.
        """


class IYearBookingOverview(IBrowserView):
    """Return overview of bookings for a year, grouped by month.
    """

    def main():
        """Get a dict with the main info.
        """

    def months_list():
        """List with info about the past twelve months
        """
    

class IDayBookingOverview(IBrowserView):
    """Return overview of bookings for a day
    """

    raw_total =  Attribute("Raw total booked hours for this day")
    total =  Attribute("Formatted total booked hours for this day")


class IXMBaseView(IBrowserView):
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

    def totals():
        """Get a dict with totals for this Story.
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

    def todo_tasks():
        """Return my to-do tasks.
        """

    def open_tasks():
        """Return my open tasks.
        """


class IEmployeeTotalsView(IBrowserView):
    """Return totals for employees
    """

    def totals():
        """Give totals
        """


class IProjectView(IXMBaseView):
    """Info about a project
    """

    def main():
        """Get a dict with info from this object.
        """
    def finished_iterations():
        """Return completed and invoiced iterations
        """

    def current_iterations():
        """Return in-progress iterations
        """

    def open_iterations():
        """Return new iterations
        """

    def non_iterations():
        """Return folder contents that are not iterations
        """
