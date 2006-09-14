# -*- coding: utf-8 -*-
#
# File: Booking.py
#
# Copyright (c) 2006 by Zest software, Lovely Systems
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
<m.van.rees@zestsoftware.nl>, Jodok Batlogg <jodok.batlogg@lovelysystems.com>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.eXtremeManagement.config import *

##code-section module-header #fill in your manual code here
BaseSchema = BaseSchema.copy()
BaseSchema['id'].widget.visible = {'edit':'hidden', 'view':'invisible'}
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
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

    DateTimeField(
        name='bookingDate',
        index="DateIndex:brains",
        widget=CalendarWidget(
            show_hm=False,
            description="Date that you worked on this task",
            label='Bookingdate',
            label_msgid='eXtremeManagement_label_bookingDate',
            description_msgid='eXtremeManagement_help_bookingDate',
            i18n_domain='eXtremeManagement',
        ),
        required=1,
        default_method=DateTime
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
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseContent,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Booking'

    meta_type = 'Booking'
    portal_type = 'Booking'
    allowed_content_types = []
    filter_content_types = 0
    global_allow = 0
    #content_icon = 'Booking.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "Booking"
    typeDescMsgId = 'description_edit_booking'

    _at_rename_after_creation = True

    schema = Booking_schema

    ##code-section class-header #fill in your manual code here

    actions=  ({'action':      '''string:${object_url}/../base_view''',
                'category':    '''object''',
                'id':          'view',
                'name':        'view',
                'permissions': ('''View''',)},
              )

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
        import transaction
        transaction.savepoint(optimistic=True)
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
        xt = getToolByName(self, 'xm_tool')
        return xt.formatTime(self.getRawActualHours())

    # Manually created methods

    security.declarePrivate('manage_afterAdd')
    def manage_afterAdd(self, item, container):
        """Reindex the parent Task when you add a Booking.
        """
        super(Booking, self).manage_afterAdd(item, container)
        self._reindexTask()

    security.declarePrivate('manage_beforeDelete')
    def manage_beforeDelete(self, item, container):
        """Reindex the parent Task when you delete a Booking.

        We need to do something like this, except that these lines
        cause Bookings to be set to 0:00 not only when they are
        deleted, but also apparently when they are moved from the
        portalFactory to their desired spot...

        self.setHours(0)
        self.setMinutes(0)
        # The following is already handled by setHours/setMinutes
        # self._reindexTask()
        """
        super(Booking, self).manage_beforeDelete(item, container)
        catalog = getToolByName(self, 'portal_catalog')
        catalog.unindexObject(self)
        self._reindexTask(reindexSelf=False)

    security.declarePrivate('_reindexTask')
    def _reindexTask(self, reindexSelf=True):
        parent = self.aq_inner.aq_parent
        cat = getToolByName(self, 'portal_catalog')
        if reindexSelf:
            # first reindex self!
            cat.reindexObject(self)
        cat.reindexObject(parent,
                          idxs=['getRawActualHours',
                                'getRawDifference'])
    security.declarePublic('setMinutes')
    def setMinutes(self, value, **kw):
        """Custom setter for minutes.

        We reindex the parent Task here so the getRawActualHours and
        getRawDifference in the catalog get updated.
        """
        self.schema['minutes'].set(self, value)
        self._reindexTask()

    security.declarePublic('setHours')
    def setHours(self, value, **kw):
        """Custom setter for hours.

        We reindex the parent Task here so the getRawActualHours and
        getRawDifference in the catalog get updated.
        """
        self.schema['hours'].set(self, value)
        self._reindexTask()



registerType(Booking, PROJECTNAME)
# end of class Booking

##code-section module-footer #fill in your manual code here
##/code-section module-footer



