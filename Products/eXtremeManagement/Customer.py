# File: Customer.py
# 
# Copyright (c) 2005 by Zest software 2005
# Generator: ArchGenXML Version 1.4.0-beta2 devel 
#            http://plone.org/products/archgenxml
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

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *




from Products.eXtremeManagement.config import *
##code-section module-header #fill in your manual code here
##/code-section module-header

schema=Schema((
    StringField('id',
        widget=StringWidget(
            label='Id',
            label_msgid='eXtremeManagement_label_id',
            description_msgid='eXtremeManagement_help_id',
            i18n_domain='eXtremeManagement',
        )
    ),

    StringField('title',
        widget=StringWidget(
            label='Title',
            label_msgid='eXtremeManagement_label_title',
            description_msgid='eXtremeManagement_help_title',
            i18n_domain='eXtremeManagement',
        )
    ),

    StringField('description',
        widget=StringWidget(
            label='Description',
            label_msgid='eXtremeManagement_label_description',
            description_msgid='eXtremeManagement_help_description',
            i18n_domain='eXtremeManagement',
        )
    ),

    StringField('name',
        widget=StringWidget(
            label='Name',
            label_msgid='eXtremeManagement_label_name',
            description_msgid='eXtremeManagement_help_name',
            i18n_domain='eXtremeManagement',
        )
    ),

    StringField('adress',
        widget=StringWidget(
            label='Adress',
            label_msgid='eXtremeManagement_label_adress',
            description_msgid='eXtremeManagement_help_adress',
            i18n_domain='eXtremeManagement',
        )
    ),

    StringField('zipCode',
        widget=StringWidget(
            label='Zipcode',
            label_msgid='eXtremeManagement_label_zipCode',
            description_msgid='eXtremeManagement_help_zipCode',
            i18n_domain='eXtremeManagement',
        )
    ),

    StringField('location',
        widget=StringWidget(
            label='Location',
            label_msgid='eXtremeManagement_label_location',
            description_msgid='eXtremeManagement_help_location',
            i18n_domain='eXtremeManagement',
        )
    ),

    StringField('country',
        widget=StringWidget(
            label='Country',
            label_msgid='eXtremeManagement_label_country',
            description_msgid='eXtremeManagement_help_country',
            i18n_domain='eXtremeManagement',
        )
    ),

    IntegerField('phoneNumber',
        widget=IntegerWidget(
            label='Phonenumber',
            label_msgid='eXtremeManagement_label_phoneNumber',
            description_msgid='eXtremeManagement_help_phoneNumber',
            i18n_domain='eXtremeManagement',
        )
    ),

    IntegerField('faxNumber',
        widget=IntegerWidget(
            label='Faxnumber',
            label_msgid='eXtremeManagement_label_faxNumber',
            description_msgid='eXtremeManagement_help_faxNumber',
            i18n_domain='eXtremeManagement',
        )
    ),

    StringField('emailAddress',
        widget=StringWidget(
            label='Emailaddress',
            label_msgid='eXtremeManagement_label_emailAddress',
            description_msgid='eXtremeManagement_help_emailAddress',
            i18n_domain='eXtremeManagement',
        )
    ),

    StringField('website',
        widget=StringWidget(
            label='Website',
            label_msgid='eXtremeManagement_label_website',
            description_msgid='eXtremeManagement_help_website',
            i18n_domain='eXtremeManagement',
        )
    ),

    StringField('comments',
        widget=StringWidget(
            label='Comments',
            label_msgid='eXtremeManagement_label_comments',
            description_msgid='eXtremeManagement_help_comments',
            i18n_domain='eXtremeManagement',
        ),
        derived="false"
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
    #content_icon               = 'Customer.gif'
    immediate_view             = 'base_view'
    default_view               = 'base_view'
    suppl_views                = ()
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



