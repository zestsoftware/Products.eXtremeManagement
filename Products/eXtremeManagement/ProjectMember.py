# File: ProjectMember.py
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
    StringField('firstName',
        widget=StringWidget(
            label='Firstname',
            label_msgid='eXtremeManagement_label_firstName',
            description_msgid='eXtremeManagement_help_firstName',
            i18n_domain='eXtremeManagement',
        )
    ),

    StringField('lastName',
        widget=StringWidget(
            label='Lastname',
            label_msgid='eXtremeManagement_label_lastName',
            description_msgid='eXtremeManagement_help_lastName',
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

    StringField('emailAddress',
        widget=StringWidget(
            label='Emailaddress',
            label_msgid='eXtremeManagement_label_emailAddress',
            description_msgid='eXtremeManagement_help_emailAddress',
            i18n_domain='eXtremeManagement',
        )
    ),

    StringField('comments',
        widget=StringWidget(
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

class ProjectMember(BaseFolder):
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseFolder,'__implements__',()),)


    # This name appears in the 'add' box
    archetype_name             = 'ProjectMember'

    meta_type                  = 'ProjectMember'
    portal_type                = 'ProjectMember'
    allowed_content_types      = ['Customer']
    filter_content_types       = 1
    global_allow               = 1
    allow_discussion           = 0
    #content_icon               = 'ProjectMember.gif'
    immediate_view             = 'base_view'
    default_view               = 'base_view'
    suppl_views                = ()
    typeDescription            = "ProjectMember"
    typeDescMsgId              = 'description_edit_projectmember'

    schema = BaseFolderSchema + \
             schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header


    #Methods

registerType(ProjectMember,PROJECTNAME)
# end of class ProjectMember

##code-section module-footer #fill in your manual code here
##/code-section module-footer



