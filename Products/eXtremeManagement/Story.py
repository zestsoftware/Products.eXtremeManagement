# File: Story.py
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

    IntegerField('attribute_25',
        widget=IntegerWidget(
            label='Attribute_25',
            label_msgid='eXtremeManagement_label_attribute_25',
            description_msgid='eXtremeManagement_help_attribute_25',
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

    StringField('mainText',
        widget=StringWidget(
            label='Maintext',
            label_msgid='eXtremeManagement_label_mainText',
            description_msgid='eXtremeManagement_help_mainText',
            i18n_domain='eXtremeManagement',
        )
    ),

),
)


##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Story(OrderedBaseFolder,BaseFolder):
    security = ClassSecurityInfo()
    __implements__ = (getattr(OrderedBaseFolder,'__implements__',()),) + (getattr(BaseFolder,'__implements__',()),)


    # This name appears in the 'add' box
    archetype_name             = 'Story'

    meta_type                  = 'Story'
    portal_type                = 'Story'
    allowed_content_types      = ['Task', 'OrderedBaseFolder', 'Story', 'Iteration', 'Project', 'ProjectFolder', 'CustomerFolder', 'Customer'] + list(getattr(OrderedBaseFolder, 'allowed_content_types', []))
    filter_content_types       = 1
    global_allow               = 0
    allow_discussion           = 0
    #content_icon               = 'Story.gif'
    immediate_view             = 'base_view'
    default_view               = 'base_view'
    suppl_views                = ()
    typeDescription            = "Story"
    typeDescMsgId              = 'description_edit_story'

    schema = BaseFolderSchema + \
             getattr(OrderedBaseFolder,'schema',Schema(())) + \
             schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header


    #Methods

registerType(Story,PROJECTNAME)
# end of class Story

##code-section module-footer #fill in your manual code here
##/code-section module-footer



