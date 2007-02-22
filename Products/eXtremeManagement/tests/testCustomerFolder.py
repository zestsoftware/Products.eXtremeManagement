# -*- coding: utf-8 -*-
#
# File: testCustomerFolder.py
#
# Copyright (c) 2006 by Zest software, Lovely Systems
# Generator: ArchGenXML 
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

__author__ = """Ahmad Hadi <a.hadi@zestsoftware.nl>, Maurits van Rees
<m.van.rees@zestsoftware.nl>, Jodok Batlogg <jodok.batlogg@lovelysystems.com>"""
__docformat__ = 'plaintext'

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

    # Manually created methods


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testCustomerFolder))
    return suite

##code-section module-footer #fill in your manual code here
##/code-section module-footer

if __name__ == '__main__':
    framework()


