from Products.eXtremeManagement.tests.base import eXtremeManagementTestCase
from Products.eXtremeManagement.content.ProjectMember import ProjectMember
from Products.eXtremeManagement.interfaces import IXMProjectMember


class testProjectMember(eXtremeManagementTestCase):
    """ test-cases for class(es) ProjectMember
    """

    def afterSetUp(self):
        """
        """
        pass

    def test_interfaces(self):
        """ Test that ProjectMember plays nice with interfaces.
        """
        self.failUnless(IXMProjectMember.implementedBy(ProjectMember))
        self.failUnless(IXMProjectMember.providedBy(ProjectMember('blah')))


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testProjectMember))
    return suite
