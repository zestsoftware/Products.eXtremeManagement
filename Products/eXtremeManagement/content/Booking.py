# File: Booking.py
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

BaseSchema = BaseSchema.copy()
BaseSchema['id'].widget.visible = {'edit':'hidden', 'view':'invisible'}
#BaseSchema['title'].widget.visible = {'edit':'hidden', 'view':'invisible'}

##/code-section module-header

schema = Schema((

    IntegerField(
        name='hours',
        index="FieldIndex",
        widget=SelectionWidget
        (
            label='Hours',
            label_msgid='eXtremeManagement_label_hours',
            i18n_domain='eXtremeManagement',
        ),
        vocabulary=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    ),

    IntegerField(
        name='minutes',
        index="FieldIndex",
        widget=SelectionWidget
        (
            label='Minutes',
            label_msgid='eXtremeManagement_label_minutes',
            i18n_domain='eXtremeManagement',
        ),
        vocabulary=(0, 15, 30, 45)
    ),

    BooleanField(
        name='billable',
        default="True",
        widget=BooleanWidget(
            label='Billable',
            label_msgid='eXtremeManagement_label_billable',
            i18n_domain='eXtremeManagement',
        )
    ),

),
)


##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Booking_schema = BaseSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Booking(BaseContent):
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseContent,'__implements__',()),)


    # This name appears in the 'add' box
    archetype_name = 'Booking'

    meta_type = 'Booking'
    portal_type = 'Booking'
    allowed_content_types = []
    filter_content_types = 0
    global_allow = 0
    allow_discussion = False
    #content_icon = 'Booking.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "Booking"
    typeDescMsgId = 'description_edit_booking'

    _at_rename_after_creation = True

    schema = Booking_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header


    # Methods
    security.declarePublic('_renameAfterCreation')
    def _renameAfterCreation(self, check_auto_id=False):
        parent = self.aq_inner.aq_parent
        maxId = 0
        for id in parent.objectIds():
            try:
                intId = int(id)
                maxId = max(maxId, intId)
            except (TypeError, ValueError):
                pass
        newId = str(maxId + 1)
        # Can't rename without a subtransaction commit when using
        # portal_factory!
        get_transaction().commit(1)
        self.setId(newId)        

    security.declarePublic('getRawActualHours')
    def getRawActualHours(self):
        """
        Get the total hours and minutes in decimal format
        for further calculations.

        HACK: If a Booking has been cancelled, it unfortunately may
        still exist, so use try/except.  The Booking should disappear
        eventually, but at least this way it doesn't give float errors
        in all sorts of scripts.
        """

        try:
            hours = float(self.getHours())
        except:
            hours = 0.0
        try:
            minutes = float(self.getMinutes())/60
        except:
            minutes = 0.0

        return hours + minutes

    security.declarePublic('getActualHours')
    def getActualHours(self):
        """
        
        """
        return self.formatTime(self.getRawActualHours())


registerType(Booking,PROJECTNAME)
# end of class Booking

##code-section module-footer #fill in your manual code here
##/code-section module-footer



