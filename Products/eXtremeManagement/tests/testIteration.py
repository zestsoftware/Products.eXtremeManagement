from Products.eXtremeManagement.tests.base import eXtremeManagementTestCase
from Products.eXtremeManagement.content.ProjectFolder import ProjectFolder


class testIteration(eXtremeManagementTestCase):
    """ test-cases for class Iteration
    """

    def test_call_iteration(self):
        """ Test that you can add and call an Iteration
        """
        self.loginAsPortalOwner()
        p=ProjectFolder('projects')
        self.portal._setObject('projects',p)
        self.setRoles(['Manager'])
        self.portal.projects.invokeFactory('Project', id='testproject01')
        self.portal.projects.testproject01.invokeFactory('Iteration', id='testIteration')
        self.failUnless('testproject01' in self.portal.projects.objectIds())
        self.failUnless('testIteration' in self.portal.projects.testproject01.objectIds())


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testIteration))
    return suite
