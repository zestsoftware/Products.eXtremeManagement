# File: eXtremeManagementTestCase.py
"""\
unknown

"""
# Copyright (c) 2005 by Zest software 2005
# Generator: ArchGenXML Version 1.4 devel 1 http://sf.net/projects/archetypes/
#
# GNU General Public Licence (GPL)
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place, Suite 330, Boston, MA  02111-1307  USA
#
__author__  = '''Ahmad Hadi <a.hadi@zestsoftware.nl>'''
__docformat__ = 'plaintext'

##code-section module-header #fill in your manual code here
##/code-section module-header

#
# Base TestCase for eXtremeManagement
#

from Products.PloneTestCase import PloneTestCase

PloneTestCase.installProduct('Archetypes')
PloneTestCase.installProduct('PortalTransforms', quiet=1)
PloneTestCase.installProduct('MimetypesRegistry', quiet=1)
PloneTestCase.installProduct('eXtremeManagement')
# If the products's config includes DEPENDENCIES, install them too
try:
    from Products.eXtremeManagement.config import DEPENDENCIES
except:
    DEPENDENCIES = []
for dependency in DEPENDENCIES:
    PloneTestCase.installProduct(dependency)

PRODUCTS = ('Archetypes', 'eXtremeManagement')

PloneTestCase.setupPloneSite(products=PRODUCTS)


class eXtremeManagementTestCase(PloneTestCase.PloneTestCase):

    ##code-section class-header_eXtremeManagementTestCase #fill in your manual code here
    ##/code-section class-header_eXtremeManagementTestCase


    def afterSetUp(self):
        pass

##code-section module-footer #fill in your manual code here
##/code-section module-footer

