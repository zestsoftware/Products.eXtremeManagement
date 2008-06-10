from Products.eXtremeManagement.tests.base import eXtremeManagementTestCase

from DateTime import DateTime

class testIteration(eXtremeManagementTestCase):
    """ test-cases for class Iteration
    """

    def test_add_iteration(self):
        """ Test that you can add an Iteration
        """

        self.setRoles(['Projectmanager'])
        self.folder.invokeFactory('Project', id='proj')
        self.folder.proj.invokeFactory('Iteration', id='it')
        self.failUnless('it' in self.folder.proj.objectIds())

    def test_iteration_start_default(self):
        """ Test that the iteration's start date is set to
        current date by default
        """
        self.setRoles(['Projectmanager'])
        self.folder.invokeFactory('Project', id='proj')
        self.folder.proj.invokeFactory('Iteration', id='it')
        it = self.folder.proj.it
        ct = DateTime()
        self.failUnless(it.startDate.year() == ct.year())
        self.failUnless(it.startDate.month() == ct.month())
        self.failUnless(it.startDate.day() == ct.day())

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testIteration))
    return suite
