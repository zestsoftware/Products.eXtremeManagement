# File: Customer.py
# 
# Copyright (c) 2005 by ['']
# Generator: ArchGenXML Version 1.4.0-beta2 http://sf.net/projects/archetypes/
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
__author__  = ''' <>'''
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

schema=Schema((
    StringField('name',
        index="FieldIndex",
        widget=StringWidget(
            description="Enter full name, eg. John Smith.",
            label='Name',
            label_msgid='eXtremeManagement_label_name',
            description_msgid='eXtremeManagement_help_name',
            i18n_domain='eXtremeManagement',
        ),
        required=1
    ),
    
    StringField('adress',
        index="FieldIndex",
        widget=StringWidget(
            description="Enter address.",
            label='Adress',
            label_msgid='eXtremeManagement_label_adress',
            description_msgid='eXtremeManagement_help_adress',
            i18n_domain='eXtremeManagement',
        ),
        required=1
    ),
    
    StringField('zipCode',
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
    
    StringField('city',
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
    
    StringField('country',
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
    
    StringField('phone',
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
    
    StringField('fax',
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
    
    StringField('email',
        index="FieldIndex",
        widget=StringWidget(
            description="Enter your email address.",
            label='Email',
            label_msgid='eXtremeManagement_label_email',
            description_msgid='eXtremeManagement_help_email',
            i18n_domain='eXtremeManagement',
        )
    ),
    
    StringField('website',
        index="FieldIndex",
        widget=StringWidget(
            description="Enter your website address.",
            label='Website',
            label_msgid='eXtremeManagement_label_website',
            description_msgid='eXtremeManagement_help_website',
            i18n_domain='eXtremeManagement',
        )
    ),
    
    TextField('comments',
        widget=TextAreaWidget(
            description="Enter some comments.",
            label='Comments',
            label_msgid='eXtremeManagement_label_comments',
            description_msgid='eXtremeManagement_help_comments',
            i18n_domain='eXtremeManagement',
        )
    ),
    
),
)


##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Customer(OrderedBaseFolder,BaseFolder):
    security = ClassSecurityInfo()
    __implements__ = (getattr(OrderedBaseFolder,'__implements__',()),) + (getattr(BaseFolder,'__implements__',()),)


    # This name appears in the 'add' box
    archetype_name             = 'Customer'

    meta_type                  = 'Customer' 
    portal_type                = 'Customer' 
    allowed_content_types      = ['ProjectMember'] + list(getattr(OrderedBaseFolder, 'allowed_content_types', []))
    filter_content_types       = 1
    global_allow               = 0
    allow_discussion           = 0
    content_icon               = 'group_icon.gif'
    immediate_view             = 'base_view'
    default_view               = 'base_view'
    typeDescription            = "Customer"
    typeDescMsgId              = 'description_edit_customer'

    schema = BaseFolderSchema + \
             getattr(OrderedBaseFolder,'schema',Schema(())) + \
             schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header


    #Methods

registerType(Customer,PROJECTNAME)
# end of class Customer

##code-section module-footer #fill in your manual code here
##/code-section module-footer



