# -*- coding: utf-8 -*-
#
# $Id$
#
# Copyright (c) 2006 by Zest Software, Lovely Systems
# Generator: ArchGenXML Version 1.5.0 svn/devel
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
<m.van.rees@zestsoftware.nl>, Jodok Batlogg
<jodok.batlogg@lovelysystems.com>, Harald Frießnegger
<harald.friessnegger@lovelysystems.com>"""
__docformat__ = 'plaintext'


##code-section init-module-header #fill in your manual code here
##/code-section init-module-header


# Subpackages
# Additional

# Classes
import IXMCustomer

##code-section init-module-footer #fill in your manual code here
import xmcustomer

from Interface.bridge import createZope3Bridge
createZope3Bridge(xmcustomer.IXMCustomer, IXMCustomer,
                  'IXMCustomer')
##/code-section init-module-footer

