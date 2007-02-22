# -*- coding: utf-8 -*-
#
# File: testCustomer.py
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

# Import the tested classes
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


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testCustomer))
    return suite

if __name__ == '__main__':
    framework()


