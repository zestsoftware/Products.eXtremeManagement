from Products.eXtremeManagement.tests.base import eXtremeManagementTestCase
from Products.eXtremeManagement.content.ProjectFolder import ProjectFolder


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


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testIteration))
    return suite
