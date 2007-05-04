from zope.interface import implements
from DateTime import DateTime
from AccessControl import ClassSecurityInfo

from Products.CMFCore.utils import getToolByName
from Products.Archetypes.atapi import *

from Products.eXtremeManagement.config import *
from Products.eXtremeManagement.interfaces import IXMBooking
from Products.eXtremeManagement.content.schemata import quarter_vocabulary, hour_vocabulary

schema = Schema((
    IntegerField(
        name='hours',
        index="FieldIndex",
        vocabulary=hour_vocabulary,
        validators=('isInt',),
        widget=SelectionWidget(
            label='Hours',
            label_msgid='eXtremeManagement_label_hours',
            i18n_domain='eXtremeManagement'),
    ),
    IntegerField(
        name='minutes',
        index="FieldIndex",
        vocabulary=quarter_vocabulary,
        validators=('isInt',),
        widget=SelectionWidget(
            label='Minutes',
            label_msgid='eXtremeManagement_label_minutes',
            i18n_domain='eXtremeManagement'),
    ),
    BooleanField(
        name='billable',
        default="True",
        widget=BooleanWidget(
            label='Billable',
            label_msgid='eXtremeManagement_label_billable',
            i18n_domain='eXtremeManagement')
    ),
    DateTimeField(
        name='bookingDate',
        index="DateIndex:brains",
        required=1,
        default_method=DateTime,
        validators=('isValidDate',),
        widget=CalendarWidget(
            show_hm=False,
            description="Date that you worked on this task",
            label='Bookingdate',
            label_msgid='eXtremeManagement_label_bookingDate',
            description_msgid='eXtremeManagement_help_bookingDate',
            i18n_domain='eXtremeManagement'),
    ),
),)

BaseSchema = BaseSchema.copy()
BaseSchema['id'].widget.visible = dict(edit=0, view=0)
Booking_schema = BaseSchema + schema


class Booking(BaseContent):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (BaseContent.__implements__,)
    implements(IXMBooking)

    # This name appears in the 'add' box
    archetype_name = 'Booking'
    portal_type = meta_type = 'Booking'
    allowed_content_types = []
    filter_content_types = 0
    global_allow = 0
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "Booking"
    typeDescMsgId = 'description_edit_booking'
    _at_rename_after_creation = True
    schema = Booking_schema

    actions=  ({'action':      '''string:${object_url}/../base_view''',
                'category':    '''object''',
                'id':          'view',
                'name':        'view',
                'permissions': ('''View''',)},
              )

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


registerType(Booking, PROJECTNAME)
