from Products.eXtremeManagement.tests.base import eXtremeManagementTestCase
from Products.eXtremeManagement.content.Project import Project
from Products.eXtremeManagement.content.ProjectFolder import ProjectFolder


class testProject(eXtremeManagementTestCase):
    """ test-cases for class Project
    """

    def afterSetUp(self):
        """
        """
        self.setRoles(['Manager'])
        self.portal.invokeFactory('ProjectFolder', id='projects')
        self.projects = self.folder.projects
        self.projects.invokeFactory('Project', id='project')
        self.project = self.projects.project

    def test_getProject(self):
        """ Test that you can add and call a Project item
        """
        self.loginAsPortalOwner()
        p=ProjectFolder('projects01')
        self.portal._setObject('projects01',p)
        self.failUnless( self.portal.projects01.portal_type == 'ProjectFolder')

        o=Project('temp_Project')
        self.portal.projects01._setObject('temp_Project', o)
        self.failUnless( self.portal.projects01.temp_Project.portal_type == 'Project')

    def test_getMembers(self):
        """
        """
        self.assertEqual(self.project.getMembers(), [])
        self.setRoles(['Manager'])
        self.membership = self.portal.portal_membership
        self.membership.addMember('employee1', 'secret', ['Employee'], [])
        self.membership.addMember('employee2', 'secret', [], [])
        self.project.manage_addLocalRoles('employee2',['Employee'])

        roleman = self.portal.acl_users.portal_role_manager
        self.assertEqual(len(roleman.listAssignedPrincipals('Employee')), 1)

        # Local roles are mentioned before global roles.
        # By default global and local roles are included.
        self.assertEqual(self.project.getMembers(), ['employee2', 'employee1'])

        self.project.update(includeGlobalMembers=False)
        self.assertEqual(self.project.getMembers(), ['employee2'])


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testProject))
    return suite
