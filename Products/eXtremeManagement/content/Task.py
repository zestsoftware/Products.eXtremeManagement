# File: Task.py
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



# additional imports from tagged value 'import'
from Products.CMFPlone.interfaces.NonStructuralFolder import INonStructuralFolder

from Products.eXtremeManagement.config import *
##code-section module-header #fill in your manual code here

from Products.CMFCore.utils import getToolByName

##/code-section module-header

schema = Schema((

    IntegerField(
        name='estimate',
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

    LinesField(
        name='assignees',
        index="FieldIndex",
        widget=MultiSelectionWidget(
            description="Select the member(s) to assign this task to.",
            label='Assignees',
            label_msgid='eXtremeManagement_label_assignees',
            description_msgid='eXtremeManagement_help_assignees',
            i18n_domain='eXtremeManagement',
        ),
        multiValued=1,
        vocabulary='_get_assignees'
    ),

    TextField(
        name='mainText',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        widget=RichWidget(
            label='Maintext',
            label_msgid='eXtremeManagement_label_mainText',
            i18n_domain='eXtremeManagement',
        ),
        default_output_type='text/html'
    ),

),
)


##code-section after-local-schema #fill in your manual code here

BaseFolderSchema = OrderedBaseFolderSchema.copy()
BaseFolderSchema['description'].isMetadata = False
BaseFolderSchema['description'].schemata = 'default'

##/code-section after-local-schema

Task_schema = BaseFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Task(BaseFolder):
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseFolder,'__implements__',()),) + (INonStructuralFolder,)


    # This name appears in the 'add' box
    archetype_name = 'Task'

    meta_type = 'Task'
    portal_type = 'Task'
    allowed_content_types = ['Booking']
    filter_content_types = 1
    global_allow = 0
    allow_discussion = True
    content_icon = 'task_icon.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "Task"
    typeDescMsgId = 'description_edit_task'

    _at_rename_after_creation = True

    schema = Task_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header


    # Methods
    security.declarePublic('_get_assignees')
    def _get_assignees(self):
        """
        returns a list of team members
        """
        portal = getToolByName(self, 'portal_url').getPortalObject()
        mem = getToolByName(self, 'portal_membership')
        uids = []
        members = self.getProject().getMembers()

        for userid in portal.acl_users.getUserIds():
            if 'Employee' in portal.acl_users.getUserById(userid).getRoles() or userid in members:
                member = mem.getMemberById(userid)
                name = hasattr(member, 'fullname') and member.fullname.strip() or member.getId()
                uids.append((userid, name))

        return DisplayList(uids)

    security.declarePublic('get_actual_hours')
    def get_actual_hours(self):
        """ Returns a float for further calculation.
        
        """  
        actual = 0.0     
        bookings = self.contentValues('Booking')
        for booking in bookings:
             actual = actual + booking.getTotal() 
        return actual

    security.declarePublic('get_actual_hours_formatted')
    def get_actual_hours_formatted(self):
        """Returns a formatted string
           e.g. 3:15
        
        """
        time = self.get_actual_hours()        
        hours = int(time)        
        minutes = int((time - hours)*60)
        if minutes == 0:
            minutes = '00'
        return ('%s:%s' % (hours, minutes))
        
    security.declarePublic('get_difference_formatted')
    def get_difference_formatted(self):
        """
        
        """
        estimated = self.getEstimate()
        actual = self.get_actual_hours()
        diff = actual - estimated
        hours = int(diff)        
        minutes = int((diff - hours)*60)
        if minutes == 0:
            minutes = '00'
        if minutes < 0:
            minutes = minutes*-1
        return ('%s:%s' % (hours, minutes))
          
    security.declarePublic('get_estimate_formatted')
    def get_estimate_formatted(self):
        """
        
        """
        estimated = self.getEstimate()
        return str(estimated) + ':00'

    security.declarePublic('CookedBody')
    def CookedBody(self):
        """
        Dummy attribute to allow drop-in replacement of Document
        """
        return self.getMainText()


registerType(Task,PROJECTNAME)
# end of class Task

##code-section module-footer #fill in your manual code here
##/code-section module-footer



