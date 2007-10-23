from Products.eXtremeManagement.tests.base import eXtremeManagementTestCase
from Products.eXtremeManagement.content.Iteration import Iteration
from Products.eXtremeManagement.content.ProjectFolder import ProjectFolder
from Products.eXtremeManagement.interfaces import IXMIteration


class testIteration(eXtremeManagementTestCase):
    """ test-cases for class(es) Iteration
    """

    def afterSetUp(self):
        """
        """
        pass

    def test_interfaces(self):
        """ Test that Iteration plays nice with interfaces.
        """
        self.failUnless(IXMIteration.implementedBy(Iteration))
        self.failUnless(IXMIteration.providedBy(Iteration('blah')))

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
