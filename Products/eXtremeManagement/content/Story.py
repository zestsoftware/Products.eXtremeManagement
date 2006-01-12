# File: Story.py
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
BaseFolderSchema['id'].widget.visible = {'edit':'hidden', 'view':'invisible'}

##/code-section module-header

schema = Schema((

    TextField(
        name='mainText',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        widget=RichWidget(
            description="Enter the main description for this object.",
            label='Maintext',
            label_msgid='eXtremeManagement_label_mainText',
            description_msgid='eXtremeManagement_help_mainText',
            i18n_domain='eXtremeManagement',
        ),
        default_output_type='text/html',
        required=1
    ),

    IntegerField(
        name='lastTaskId',
        default="0",
        widget=IntegerWidget(
            visible={'edit' : 'invisible', 'view' : 'visible' } ,
            label='Lasttaskid',
            label_msgid='eXtremeManagement_label_lastTaskId',
            description_msgid='eXtremeManagement_help_lastTaskId',
            i18n_domain='eXtremeManagement',
        )
    ),

),
)


##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Story_schema = OrderedBaseFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Story(OrderedBaseFolder):
    security = ClassSecurityInfo()
    __implements__ = (getattr(OrderedBaseFolder,'__implements__',()),)


    # This name appears in the 'add' box
    archetype_name = 'Story'

    meta_type = 'Story'
    portal_type = 'Story'
    allowed_content_types = ['Task']
    filter_content_types = 1
    global_allow = 0
    allow_discussion = False
    content_icon = 'story_icon.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "Story"
    typeDescMsgId = 'description_edit_story'

    _at_rename_after_creation = True

    schema = Story_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header


    # Methods
    security.declarePublic('CookedBody')
    def CookedBody(self):
        """
        Dummy attribute to allow drop-in replacement of Document
        """
        return self.getMainText()

    security.declarePublic('get_progress_perc')
    def get_progress_perc(self):
        """
        
        """
        tasks = self.contentValues()
        estimates = []
        actual = 0.0
        if tasks:
            for task in tasks:
                estimates.append(task.getEstimate())
                actual = actual + task.get_actual_hours()
            estimated = sum(estimates)
            if estimated > 0:
                return round(actual/estimated*100, 1)
            else:
                return 0.0
        else:
            return 0

    # Manually created methods

    def generateUniqueId(self, type_name):
        """ Generate sequential IDs for tasks
        With thanks to Upfront Systems for their code from Upfront Project
        """
        if type_name == 'Task':
            self.lastTaskId += 1
            return str(self.lastTaskId)
        else:
            return self.aq_parent.generateUniqueId(type_name)



registerType(Story,PROJECTNAME)
# end of class Story

##code-section module-footer #fill in your manual code here
##/code-section module-footer



