# File: Task.py
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

    IntegerField('attribute_33',
        widget=IntegerWidget(
            label='Attribute_33',
            label_msgid='eXtremeManagement_label_attribute_33',
            description_msgid='eXtremeManagement_help_attribute_33',
            i18n_domain='eXtremeManagement',
        )
    ),

    IntegerField('estimate',
        widget=IntegerWidget(
            label='Estimate',
            label_msgid='eXtremeManagement_label_estimate',
            description_msgid='eXtremeManagement_help_estimate',
            i18n_domain='eXtremeManagement',
        )
    ),

    IntegerField('actual',
        widget=IntegerWidget(
            label='Actual',
            label_msgid='eXtremeManagement_label_actual',
            description_msgid='eXtremeManagement_help_actual',
            i18n_domain='eXtremeManagement',
        )
    ),

    StringField('assignTo',
        widget=SelectionWidget(
            label='Assignto',
            label_msgid='eXtremeManagement_label_assignTo',
            description_msgid='eXtremeManagement_help_assignTo',
            i18n_domain='eXtremeManagement',
        )
    ),

),
)


##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Task(BaseContent):
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseContent,'__implements__',()),)


    # This name appears in the 'add' box
    archetype_name             = 'Task'

    meta_type                  = 'Task'
    portal_type                = 'Task'
    allowed_content_types      = []
    filter_content_types       = 0
    global_allow               = 0
    allow_discussion           = 0
    #content_icon               = 'Task.gif'
    immediate_view             = 'base_view'
    default_view               = 'base_view'
    suppl_views                = ()
    typeDescription            = "Task"
    typeDescMsgId              = 'description_edit_task'

    schema = BaseSchema + \
             schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header


    #Methods

registerType(Task,PROJECTNAME)
# end of class Task

##code-section module-footer #fill in your manual code here
##/code-section module-footer



