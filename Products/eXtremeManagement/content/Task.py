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
from Products.eXtremeManagement.config import *

# additional imports from tagged value 'import'
from Products.CMFPlone.interfaces.NonStructuralFolder import INonStructuralFolder

##code-section module-header #fill in your manual code here

from Products.CMFCore.utils import getToolByName
from sets import Set
from Products.eXtremeManagement.Extensions.eXtreme_Task_Workflow_scripts import mailMessage

##/code-section module-header

schema = Schema((

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

    IntegerField(
        name='hours',
        default="0",
        index="FieldIndex",
        widget=IntegerWidget(
            description="Enter the estimated time (in hours).",
            label='Hours',
            label_msgid='eXtremeManagement_label_hours',
            description_msgid='eXtremeManagement_help_hours',
            i18n_domain='eXtremeManagement',
        )
    ),

    IntegerField(
        name='minutes',
        default="0",
        index="FieldIndex",
        widget=SelectionWidget
        (
            label='Minutes',
            label_msgid='eXtremeManagement_label_minutes',
            i18n_domain='eXtremeManagement',
        ),
        vocabulary=(0, 15, 30, 45)
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
    __implements__ = (getattr(BaseFolder,'__implements__',()),)

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

        users = {}
        current = portal.aq_inner
        while current is not None:
            if hasattr(current, 'aq_base') and hasattr(current.aq_base, 'acl_users'):
                for user in current.acl_users.getUsers():
                    userid = user.getId()
                    roles = users.get(userid, None)
                    if roles is None:
                        roles = Set()
                        users[userid] = roles
                    roles.update(user.getRoles())
            current = getattr(current, 'aq_parent', None)
            
        possibleUids = list(users.keys())
        possibleUids.sort()
        for userid in possibleUids:
            if 'Employee' in users[userid] or userid in members:
                member = mem.getMemberById(userid)
                if member is not None:
                    name = hasattr(member, 'fullname') and member.fullname.strip() or member.getId()
                    uids.append((userid, name))

        return DisplayList(uids)

    security.declarePublic('setAssignees')
    def setAssignees(self, value, **kw):
        """
        Overwrite the default setter.  An email should be sent on assignment.
        """
        self.schema['assignees'].set(self, value)
        portal = getToolByName(self, 'portal_url').getPortalObject()
        mailMessage(portal, self, 'New Task assigned')

    security.declarePublic('getRawEstimate')
    def getRawEstimate(self):
        """
        Return hours + minutes as a single float.
        """
        return self.getHours() + (self.getMinutes() / 60.0)
        
    security.declarePublic('getEstimate')
    def getEstimate(self):
        """
        Return the formatted estimate.
        """
        return self.formatTime(self.getRawEstimate())

    security.declarePublic('getRawActualHours')
    def getRawActualHours(self):
        """ Returns a float for further calculation.
        
        """  
        actual = 0.0     
        bookings = self.contentValues('Booking')
        for booking in bookings:
             actual = actual + booking.getRawActualHours()
        return actual

    security.declarePublic('getActualHours')
    def getActualHours(self):
        """Returns a formatted string
           e.g. 3:15
        """
        return self.formatTime(self.getRawActualHours())

    security.declarePublic('getRawDifference')
    def getRawDifference(self):
        """
        
        """
        return self.getRawActualHours() -  self.getRawEstimate()
          
    security.declarePublic('getDifference')
    def getDifference(self):
        """
        
        """
        return self.formatTime(self.getRawDifference())

    security.declarePublic('CookedBody')
    def CookedBody(self):
        """
        Dummy attribute to allow drop-in replacement of Document
        """
        return self.getMainText()

    security.declarePublic('startable')
    def startable(self):
        """
        A task should have an assignee and an estimate.
        """
        if self.getAssignees() and self.getRawEstimate() > 0:
            return True
        else:
            return False


registerType(Task,PROJECTNAME)
# end of class Task

##code-section module-footer #fill in your manual code here
##/code-section module-footer



