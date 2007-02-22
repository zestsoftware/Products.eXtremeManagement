# -*- coding: utf-8 -*-
#
# File: testIteration.py
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


from Products.eXtremeManagement.content.Iteration import Iteration
from Products.eXtremeManagement.content.ProjectFolder import ProjectFolder
from Products.eXtremeManagement.interfaces import IXMIteration


class testIteration(eXtremeManagementTestCase):
    """ test-cases for class(es) Iteration
    """

    def afterSetUp(self):
        """
        """
        pass

    def test_interfaces(self):
        """ Test that Iteration plays nice with interfaces.
        """
        self.failUnless(IXMIteration.implementedBy(Iteration))

    def test_call_iteration(self):
        """ Test that you can add and call an Iteration
        """
        self.loginAsPortalOwner()
        p=ProjectFolder('projects')
        self.portal._setObject('projects',p)
        self.setRoles(['Manager'])
        self.portal.projects.invokeFactory('Project', id='testproject01')
        self.portal.projects.testproject01.invokeFactory('Iteration', id='testIteration')
        self.failUnless('testproject01' in self.portal.projects.objectIds())
        self.failUnless('testIteration' in self.portal.projects.testproject01.objectIds())


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testIteration))
    return suite

##code-section module-footer #fill in your manual code here
##/code-section module-footer

if __name__ == '__main__':
    framework()


