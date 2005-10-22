# File: Booking.py
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

BaseSchema = BaseSchema.copy()
BaseSchema['id'].widget.visible = {'edit':'hidden', 'view':'invisible'}
#BaseSchema['title'].widget.visible = {'edit':'hidden', 'view':'invisible'}

##/code-section module-header

schema=Schema((
    IntegerField('hours',
        index="FieldIndex",
        widget=SelectionWidget
        (
            label='Hours',
            label_msgid='eXtremeManagement_label_hours',
            description_msgid='eXtremeManagement_help_hours',
            i18n_domain='eXtremeManagement',
        ),
        vocabulary=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    ),

    IntegerField('minutes',
        index="FieldIndex",
        widget=SelectionWidget
        (
            label='Minutes',
            label_msgid='eXtremeManagement_label_minutes',
            description_msgid='eXtremeManagement_help_minutes',
            i18n_domain='eXtremeManagement',
        ),
        vocabulary=(0, 15, 30, 45)
    ),

    BooleanField('billable',
        default="True",
        widget=BooleanWidget(
            label='Billable',
            label_msgid='eXtremeManagement_label_billable',
            description_msgid='eXtremeManagement_help_billable',
            i18n_domain='eXtremeManagement',
        )
    ),

),
)


##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Booking_schema = BaseSchema + \
    schema

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Booking(BaseContent):
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseContent,'__implements__',()),)


    # This name appears in the 'add' box
    archetype_name             = 'Booking'

    meta_type                  = 'Booking'
    portal_type                = 'Booking'
    allowed_content_types      = []
    filter_content_types       = 0
    global_allow               = 0
    allow_discussion           = 0
    #content_icon               = 'Booking.gif'
    immediate_view             = 'base_view'
    default_view               = 'base_view'
    suppl_views                = ()
    typeDescription            = "Booking"
    typeDescMsgId              = 'description_edit_booking'

    _at_rename_after_creation  = True

    schema = Booking_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header


    #Methods

    security.declarePublic('getTotal')
    def getTotal(self):
        """ Get the total hours and minutes in decimal format
            for further calculations.
        
        """
        hours = float(self.getHours())
        minutes = float(self.getMinutes())/60
        return hours + minutes



    security.declarePublic('getTotalFormatted')
    def getTotalFormatted(self):
        """ Get the Total hours and minutes as a formatted
            string e.g. 3:15
        
        """
        minutes = self.getMinutes()
        if minutes == 0:
            minutes = '00'
        else:
            minutes = str(minutes)
        return str(self.getHours()) + ':' + minutes



registerType(Booking,PROJECTNAME)
# end of class Booking

##code-section module-footer #fill in your manual code here
##/code-section module-footer



