# File: Customer.py
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


from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *



from Products.eXtremeManagement.config import *
##code-section module-header #fill in your manual code here

BaseFolderSchema = OrderedBaseFolderSchema.copy()
OrderedBaseFolderSchema['description'].isMetadata = False
OrderedBaseFolderSchema['description'].schemata = 'default'
OrderedBaseFolderSchema['id'].widget.visible = {'edit':'hidden', 'view':'invisible'}

##/code-section module-header

schema = Schema((

    StringField(
        name='name',
        index="FieldIndex",
        widget=StringWidget(
            description="Enter the company name for this customer",
            label='Name',
            label_msgid='eXtremeManagement_label_name',
            description_msgid='eXtremeManagement_help_name',
            i18n_domain='eXtremeManagement',
        ),
        required=1
    ),

    StringField(
        name='address',
        index="FieldIndex",
        widget=StringWidget(
            description="Enter address.",
            label='Address',
            label_msgid='eXtremeManagement_label_address',
            description_msgid='eXtremeManagement_help_address',
            i18n_domain='eXtremeManagement',
        ),
        required=1
    ),

    StringField(
        name='zipCode',
        index="FieldIndex",
        widget=StringWidget(
            description="Enter zip code.",
            label='Zipcode',
            label_msgid='eXtremeManagement_label_zipCode',
            description_msgid='eXtremeManagement_help_zipCode',
            i18n_domain='eXtremeManagement',
        ),
        required=1
    ),

    StringField(
        name='city',
        index="FieldIndex",
        widget=StringWidget(
            description="Enter city name.",
            label='City',
            label_msgid='eXtremeManagement_label_city',
            description_msgid='eXtremeManagement_help_city',
            i18n_domain='eXtremeManagement',
        ),
        required=1
    ),

    StringField(
        name='country',
        index="FieldIndex",
        widget=StringWidget(
            description="Enter country.",
            label='Country',
            label_msgid='eXtremeManagement_label_country',
            description_msgid='eXtremeManagement_help_country',
            i18n_domain='eXtremeManagement',
        ),
        required=1
    ),

    StringField(
        name='phone',
        index="FieldIndex",
        widget=IntegerWidget
        (
            size="30",
            description="Enter your phone number.",
            label='Phone',
            label_msgid='eXtremeManagement_label_phone',
            description_msgid='eXtremeManagement_help_phone',
            i18n_domain='eXtremeManagement',
        ),
        required=1
    ),

    StringField(
        name='fax',
        index="FieldIndex",
        widget=IntegerWidget
        (
            size="30",
            description="Enter your fax number.",
            label='Fax',
            label_msgid='eXtremeManagement_label_fax',
            description_msgid='eXtremeManagement_help_fax',
            i18n_domain='eXtremeManagement',
        )
    ),

    StringField(
        name='website',
        index="FieldIndex",
        widget=StringWidget(
            description="Enter your website address.",
            label='Website',
            label_msgid='eXtremeManagement_label_website',
            description_msgid='eXtremeManagement_help_website',
            i18n_domain='eXtremeManagement',
        )
    ),

),
)


##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Customer_schema = OrderedBaseFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here

Customer_schema = schema + BaseFolderSchema 

##/code-section after-schema

class Customer(OrderedBaseFolder):
    security = ClassSecurityInfo()
    __implements__ = (getattr(OrderedBaseFolder,'__implements__',()),)


    # This name appears in the 'add' box
    archetype_name = 'Customer'

    meta_type = 'Customer'
    portal_type = 'Customer'
    allowed_content_types = ['ProjectMember']
    filter_content_types = 1
    global_allow = 0
    allow_discussion = False
    content_icon = 'group_icon.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "Customer"
    typeDescMsgId = 'description_edit_customer'

    actions =  (


       {'action': "string:${object_url}/folder_localrole_form",
        'category': "object",
        'id': 'local_roles',
        'name': 'Sharing',
        'permissions': ("View",),
        'condition': 'python:1'
       },


    )

    _at_rename_after_creation = True

    schema = Customer_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header


    # Methods

registerType(Customer,PROJECTNAME)
# end of class Customer

##code-section module-footer #fill in your manual code here
##/code-section module-footer



