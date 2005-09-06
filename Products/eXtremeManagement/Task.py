# File: Task.py
# 
# Copyright (c) 2005 by Zest software 2005
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
__author__  = '''Ahmad Hadi <a.hadi@zestsoftware.nl>'''
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *




from Products.eXtremeManagement.config import *
##code-section module-header #fill in your manual code here
##/code-section module-header

schema=Schema((
    TextField('task',
        index="FieldIndex",
        widget=TextAreaWidget(
            description="Enter task description.",
            label='Task',
            label_msgid='eXtremeManagement_label_task',
            description_msgid='eXtremeManagement_help_task',
            i18n_domain='eXtremeManagement',
        ),
        required=1
    ),
    
    IntegerField('estimate',
        default="0",
        index="FieldIndex",
        widget=IntegerWidget(
            description="Enter the estimated time (in hours).",
            label='Estimate',
            label_msgid='eXtremeManagement_label_estimate',
            description_msgid='eXtremeManagement_help_estimate',
            i18n_domain='eXtremeManagement',
        ),
        required=1
    ),
    
    IntegerField('actual',
        default="0",
        index="FieldIndex",
        widget=IntegerWidget(
            description="Enter the actual time (in hours).",
            label='Actual',
            label_msgid='eXtremeManagement_label_actual',
            description_msgid='eXtremeManagement_help_actual',
            i18n_domain='eXtremeManagement',
        )
    ),
    
    LinesField('assignees',
        index="FieldIndex",
        widget=MultiSelectionWidget(
            description="Select the member(s) to assign this task to.",
            label='Assignees',
            label_msgid='eXtremeManagement_label_assignees',
            description_msgid='eXtremeManagement_help_assignees',
            i18n_domain='eXtremeManagement',
        ),
        multiValued=1
    ),
    
),
)


##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Task(OrderedBaseFolder,BaseContent):
    security = ClassSecurityInfo()
    __implements__ = (getattr(OrderedBaseFolder,'__implements__',()),) + (getattr(BaseContent,'__implements__',()),)


    # This name appears in the 'add' box
    archetype_name             = 'Task'

    meta_type                  = 'Task' 
    portal_type                = 'Task' 
    allowed_content_types      = [] + list(getattr(OrderedBaseFolder, 'allowed_content_types', []))
    filter_content_types       = 0
    global_allow               = 0
    allow_discussion           = 0
    #content_icon               = 'Task.gif'
    immediate_view             = 'base_view'
    default_view               = 'base_view'
    typeDescription            = "Task"
    typeDescMsgId              = 'description_edit_task'

    schema = BaseSchema + \
             getattr(OrderedBaseFolder,'schema',Schema(())) + \
             schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header


    #Methods

registerType(Task,PROJECTNAME)
# end of class Task

##code-section module-footer #fill in your manual code here
##/code-section module-footer



