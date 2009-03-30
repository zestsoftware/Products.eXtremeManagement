from zope.interface import Attribute
from zope.publisher.interfaces.browser import IBrowserView


class IProjects(IBrowserView):
    """Manage all active projects.
    """

    def projects():
        pass


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

    def raw_total():
        """Raw total booked hours for this day.
        """

    def total():
        """Formatted total booked hours for this day.
        """


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

    def tasklist():
        """Return the Tasks of this Story
        """

    def task_titles_not_startable():
        """Titles of the tasks that cannot be started.
        """

    def show_add_task_form():
        """Return whether the add task form should be shown or not"""

    def get_possible_assignees():
        """Return a list of (id, name, selected) tuples of employees which
        can be assigned to tasks in this story.
        The selected element can be used to determine the default assignee.
        """


class IIterationView(IXMBaseView):
    """Info about an iteration
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

    def story_titles_not_startable():
        """Titles of the tasks that cannot be started.
        """

    def actual_budget_left():
        """Return the hours left in the project.
        """

    def second_current_iteration():
        """ Return the url of a second iteration with status in-progress
        """


class IOfferView(IIterationView):
    """Info about an offer.
    """

    def main():
        """Get a dict with info from this object.
        """

    def stories():
        """Return the Stories of this Offer.
        """

    def show_draft():
        """Return whether draft state of stories should be shown in the view.
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

    def current_iterations():
        """Return in-progress iterations
        """

    def attachments():
        """Return folder contents that are not iterations
        """

    def offers():
        """ Return a list of dicts with title and url of offers
        """


class IXMGlobalState(IBrowserView):
    """Global information about eXtremeManagement.

    Global here means: it is the same for all contexts.
    """

    def has_tracker():
        """Is the xm time tracker package available?"""


class IEmployeesView(IBrowserView):
    """A view which displays all employees and their billable percentages
    per month.
    """

    def items():
        """ Returns a list of months each month contains a list of employees
        and each employee is a dict.

        [{'month':'April',
          'employees':[
              {'name':'Mark van Lent',
               'month_url': 'http://example.com/booking_month?memberid=mark',
               'percentage': '70 %'},
              {'name':'Mark van Lent',
               'month_url': 'http://example.com/booking_month?memberid=mark',
               'percentage': '70 %'},
                      ],
        ]
        """
