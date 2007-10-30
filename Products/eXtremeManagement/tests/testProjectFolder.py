from Products.eXtremeManagement.tests.base import eXtremeManagementTestCase
from Products.eXtremeManagement.content.ProjectFolder import ProjectFolder


class testProjectFolder(eXtremeManagementTestCase):
    """ test-cases for class ProjectFolder
    """

    def test_projectFolder(self):
        """Test adding a ProjectFolder.  And adding a Project in that.
        """
        self.setRoles(['Projectmanager'])
        self.folder.invokeFactory('ProjectFolder', id='projects')
        self.failUnless(self.folder.projects.portal_type == 'ProjectFolder')

        self.folder.projects.invokeFactory('Project', id='project')
        self.failUnless(self.folder.projects.project.portal_type == 'Project')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testProjectFolder))
    return suite
