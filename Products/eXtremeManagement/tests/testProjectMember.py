import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing import ZopeTestCase

from Products.eXtremeManagement.config import *
from Products.eXtremeManagement.tests.eXtremeManagementTestCase import eXtremeManagementTestCase
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


if __name__ == '__main__':
    framework()


