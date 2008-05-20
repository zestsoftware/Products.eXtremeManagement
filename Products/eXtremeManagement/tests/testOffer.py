from Products.eXtremeManagement.tests.base import eXtremeManagementTestCase


class testOffer(eXtremeManagementTestCase):
    """ test-cases for class Offer
    """

    def test_add_offer(self):
        """ Test that you can add an Offer
        """

        self.setRoles(['Projectmanager'])
        self.folder.invokeFactory('Project', id='proj')
        self.folder.proj.invokeFactory('Offer', id='of')
        self.failUnless('of' in self.folder.proj.objectIds())


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testOffer))
    return suite
