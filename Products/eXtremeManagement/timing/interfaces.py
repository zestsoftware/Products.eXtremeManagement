from zope.interface import Interface
from zope.interface import Attribute
from zope.annotation.interfaces import IAttributeAnnotatable


class IActualHoursContainer(IAttributeAnnotatable):
    """Marker interface: this object has children with actual hours
    """

    def contentValues():
        """List the content objects in this container
        """


class IActualHours(Interface):
    """Actual hours and minutes worked
    """

    actual_time = Attribute("Actual time")

    def recalc():
        """Recalculate the total of bookings/actual hours.
        """


class IEstimateContainer(IAttributeAnnotatable):
    """Marker interface: this object has children with estimates
    """

    def contentValues():
        """List the content objects in this container
        """


class IEstimate(Interface):
    """Estimated time to work
    """

    estimate = Attribute("Estimate")

    def recalc():
        """Recalculate the total of estimates
        """


class ISizeEstimate(Interface):
    """Estimated size of work load

    Think Story Points or Ideal Days
    """

    size_estimate = Attribute("Size Estimate")

    def recalc():
        """Recalculate the total of size estimates
        """
