import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing import ZopeTestCase

from Products.eXtremeManagement.config import *
from Products.eXtremeManagement.tests.eXtremeManagementTestCase import eXtremeManagementTestCase
from Products.eXtremeManagement.content.CustomerFolder import CustomerFolder
from Products.eXtremeManagement.interfaces import IXMCustomerFolder


class testCustomerFolder(eXtremeManagementTestCase):
    """ test-cases for class(es) CustomerFolder
    """

    def afterSetUp(self):
        """
        """
        pass

    def test_interfaces(self):
        """ Test that CustomerFolder plays nice with interfaces.
        """
        self.failUnless(IXMCustomerFolder.implementedBy(CustomerFolder))
        self.failUnless(IXMCustomerFolder.providedBy(CustomerFolder('blah')))

    def test_call_customerFolder(self):
        """ Test if the customers folder is created
        """
        self.loginAsPortalOwner()
        c=CustomerFolder('customers')
        self.portal._setObject('customers',c)
        self.failUnless('customers' in self.portal.objectIds())
        self.failUnless( self.portal.customers.portal_type == 'CustomerFolder')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testCustomerFolder))
    return suite


if __name__ == '__main__':
    framework()
