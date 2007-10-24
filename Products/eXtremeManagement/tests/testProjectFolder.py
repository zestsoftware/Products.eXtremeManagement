from Products.eXtremeManagement.tests.base import eXtremeManagementTestCase
from Products.eXtremeManagement.content.ProjectFolder import ProjectFolder


class testProjectFolder(eXtremeManagementTestCase):
    """ test-cases for class(es) ProjectFolder
    """

    def afterSetUp(self):
        """
        """
        self.setRoles(['Manager'])
        self.portal.invokeFactory('ProjectFolder', id='projects')
        self.projects = self.folder.projects

        self.projects.invokeFactory('Project', id='project')
        self.project = self.projects.project

    def test_projectFolder(self):
        """Test adding a ProjectFolder in the portal root
        """
        self.loginAsPortalOwner()
        p=ProjectFolder('projects01')
        self.portal._setObject('projects01',p)
        self.failUnless( self.portal.projects01.portal_type == 'ProjectFolder')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testProjectFolder))
    return suite
