# File: eXtremeManagementTestCase.py
#
# Copyright (c) 2006 by Zest software
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
<m.van.rees@zestsoftware.nl>"""
__docformat__ = 'plaintext'

#
# Base TestCase for eXtremeManagement
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

##code-section module-header #fill in your manual code here
##/code-section module-header

from Testing import ZopeTestCase
from Products.PloneTestCase import PloneTestCase
from Products.eXtremeManagement.config import HAS_PLONE21
from Products.eXtremeManagement.config import PRODUCT_DEPENDENCIES
from Products.eXtremeManagement.config import DEPENDENCIES

# Add common dependencies
if not HAS_PLONE21:
    DEPENDENCIES.append('Archetypes')
    PRODUCT_DEPENDENCIES.append('MimetypesRegistry')
    PRODUCT_DEPENDENCIES.append('PortalTransforms')
PRODUCT_DEPENDENCIES.append('eXtremeManagement')

# Install all (product-) dependencies, install them too
for dependency in PRODUCT_DEPENDENCIES + DEPENDENCIES:
    ZopeTestCase.installProduct(dependency)

ZopeTestCase.installProduct('eXtremeManagement')

PRODUCTS = list()
PRODUCTS += DEPENDENCIES
PRODUCTS.append('eXtremeManagement')

testcase = PloneTestCase.PloneTestCase

##code-section module-before-plone-site-setup #fill in your manual code here
##/code-section module-before-plone-site-setup

PloneTestCase.setupPloneSite(products=PRODUCTS)

class eXtremeManagementTestCase(testcase):
    """Base TestCase for eXtremeManagement."""

    ##code-section class-header_eXtremeManagementTestCase #fill in your manual code here
    ##/code-section class-header_eXtremeManagementTestCase

    # Commented out for now, it gets blasted at the moment anyway.
    # Place it in the protected section if you need it.
    #def afterSetup(self):
    #    """
    #    """
    #    pass


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(eXtremeManagementTestCase))
    return suite

##code-section module-footer #fill in your manual code here
##/code-section module-footer

if __name__ == '__main__':
    framework()


