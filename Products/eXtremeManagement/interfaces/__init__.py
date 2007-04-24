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

__author__ = """Ahmad Hadi <a.hadi@zestsoftware.nl>,
Maurits van Rees <m.van.rees@zestsoftware.nl>,
Jodok Batlogg <jodok.batlogg@lovelysystems.com>,
Harald Frießnegger <harald.friessnegger@lovelysystems.com>"""
__docformat__ = 'plaintext'


import IXMCustomer as IXMCustomerZope2

from xmcustomerfolder import IXMCustomerFolder
from xmcustomer import IXMCustomer
from xmprojectmember import IXMProjectMember
from xmprojectfolder import IXMProjectFolder
from xmproject import IXMProject
from xmiteration import IXMIteration
from xmstory import IXMStory
from xmtask import IXMTask
from xmbooking import IXMBooking

our_interfaces = (
    IXMCustomerFolder,
    IXMCustomer,
    IXMProjectMember,
    IXMProjectFolder,
    IXMProject,
    IXMIteration,
    IXMStory,
    IXMTask,
    IXMBooking,
    )

from zope.interface import alsoProvides
from zope.app.content.interfaces import IContentType

for iface in our_interfaces:
    alsoProvides(iface, IContentType)

# Only add zope 3 bridges if you somehow need them.
# If this gets removed by someone who knows what he is doing, that is
# fine with me.  [Maurits.]
from Interface.bridge import createZope3Bridge
createZope3Bridge(IXMCustomer, IXMCustomerZope2,
                  'IXMCustomer')

