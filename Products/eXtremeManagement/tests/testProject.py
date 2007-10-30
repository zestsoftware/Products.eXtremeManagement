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
        """ Test that you can add and a Project item.

        Well, we added it already; we just need to test if a proper
        object is there.
        """
        self.failUnless(self.portal.projects.project.portal_type == 'Project')

    def test_getMembers(self):
        """
        """
        self.assertEqual(self.project.getMembers(), [])
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
