from Products.eXtremeManagement.tests.base import eXtremeManagementTestCase


class testProject(eXtremeManagementTestCase):
    """ test-cases for class Project
    """

    def afterSetUp(self):
        """
        """
        self.setRoles(['Manager'])
        self.project = self.portal.project

    def test_getProject(self):
        """ Test that you can add and a Project item.

        Well, we added it already; we just need to test if a proper
        object is there.
        """
        self.failUnless(self.project.portal_type == 'Project')

    def test_getMembers(self):
        """
        """
        # We already have some Employees, twoglobal and one local.
        self.assertEqual(self.project.getMembers(),
                         ['test_user_1_', 'developer', 'employee'])

        roleman = self.portal.acl_users.portal_role_manager
        self.assertEqual(len(roleman.listAssignedPrincipals('Employee')), 2)

        # Local roles are mentioned before global roles.
        # By default global and local roles are included.
        self.assertEqual(
            self.project.getMembers(),
            ['test_user_1_', 'developer', 'employee'])

        self.project.update(includeGlobalMembers=False)
        self.assertEqual(self.project.getMembers(), ['test_user_1_'])

    def test_budgetHours(self):
        """Test the setter and  getter of the budget hours.
        """
        self.project.setBudgetHours(40.5)
        self.assertEqual(self.project.getBudgetHours(), 40.5)

    def test_budgetHoursPermissions(self):
        """Test the 'Edit budgetHours' permission for several roles.
        """
        # We have already added some users with global roles.
        membership = self.portal.portal_membership

        # We should be able to set the budget hours as Manager
        self.login('manager')
        self.failUnless(membership.checkPermission(
            'eXtremeManagement: Edit budgetHours', self.project))

        # We should be able to set the budget hours as Projectmanager
        self.login('projectmanager')
        self.failUnless(membership.checkPermission(
            'eXtremeManagement: Edit budgetHours', self.project))

        # We should NOT be able to set the budget hours as Employee
        self.login('employee')
        self.failIf(membership.checkPermission(
            'eXtremeManagement: Edit budgetHours', self.project))

        # We should NOT be able to set the budget hours as Customer
        self.login('customer')
        self.failIf(membership.checkPermission(
            'eXtremeManagement: Edit budgetHours', self.project))

        # We should NOT be able to set the budget hours as Member
        self.login('member')
        self.failIf(membership.checkPermission(
            'eXtremeManagement: Edit budgetHours', self.project))


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testProject))
    return suite
