from Products.eXtremeManagement.tests.base import eXtremeManagementTestCase
from Products.eXtremeManagement.content.Customer import Customer
from Products.eXtremeManagement.interfaces import IXMCustomer


class testCustomer(eXtremeManagementTestCase):
    """ test-cases for class(es) Customer
    """

    def afterSetUp(self):
        """
        """
        pass

    def test_interfaces(self):
        """ Test that Customer plays nice with interfaces.
        """
        self.failUnless(IXMCustomer.implementedBy(Customer))
        self.failUnless(IXMCustomer.providedBy(Customer('blah')))


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testCustomer))
    return suite
