from Products.eXtremeManagement.tests.base import eXtremeManagementTestCase
from xm.booking.timing.interfaces import IActualHours


class testBooking(eXtremeManagementTestCase):
    """ test-cases for class Booking
    """

    def test_ActualHours(self):
        """
        """
        task = self.portal.project.iteration.story.task
        booking = task.booking
        ann = IActualHours(booking)
        self.assertEqual(ann.actual_time, 3.25)

        task.invokeFactory('Booking', id='booking2', hours=0, minutes=0)
        ann = IActualHours(task.booking2)
        self.assertEqual(ann.actual_time, 0.0)

        task.invokeFactory('Booking', id='booking3', hours=0, minutes=45)
        ann = IActualHours(task.booking3)
        self.assertEqual(ann.actual_time, 0.75)

        # The following two have a weird number of minutes, but if
        # they pass, that is fine.
        task.invokeFactory('Booking', id='booking4', hours=4, minutes=60)
        ann = IActualHours(task.booking4)
        self.assertEqual(ann.actual_time, 5.0)

        task.invokeFactory('Booking', id='booking5', hours=4, minutes=75)
        ann = IActualHours(task.booking5)
        self.assertEqual(ann.actual_time, 5.25)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testBooking))
    return suite
