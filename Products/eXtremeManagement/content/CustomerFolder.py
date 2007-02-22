# -*- coding: utf-8 -*-
#
# File: CustomerFolder.py
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

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.eXtremeManagement.config import *

from zope.interface import implements
from Products.eXtremeManagement.interfaces import IXMCustomerFolder

from Products.CMFCore.permissions import ManageProperties
BaseFolderSchema = OrderedBaseFolderSchema.copy()
OrderedBaseFolderSchema['description'].isMetadata = False
OrderedBaseFolderSchema['description'].schemata = 'default'


schema = Schema((

),
)

CustomerFolder_schema = OrderedBaseFolderSchema.copy() + \
    schema.copy()


class CustomerFolder(OrderedBaseFolder):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(OrderedBaseFolder,'__implements__',()),)
    implements(IXMCustomerFolder)

    # This name appears in the 'add' box
    archetype_name = 'CustomerFolder'

    meta_type = 'CustomerFolder'
    portal_type = 'CustomerFolder'
    allowed_content_types = ['Customer']
    filter_content_types = 1
    global_allow = 1
    content_icon = 'group_icon.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "CustomerFolder"
    typeDescMsgId = 'description_edit_customerfolder'

    actions =  (

        {
        'id'          : 'local_roles',
        'name'        : 'Sharing',
        'action'      : 'string:${object_url}/folder_localrole_form',
        'permissions' : (ManageProperties,),
         },


        )

    _at_rename_after_creation = True

    schema = CustomerFolder_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods


registerType(CustomerFolder, PROJECTNAME)
# end of class CustomerFolder

##code-section module-footer #fill in your manual code here
##/code-section module-footer



