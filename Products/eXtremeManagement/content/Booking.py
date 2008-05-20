from zope.interface import implements
from DateTime import DateTime
from AccessControl import ClassSecurityInfo

from Products.Archetypes.atapi import Schema
from Products.Archetypes.atapi import IntegerField
from Products.Archetypes.atapi import SelectionWidget
from Products.Archetypes.atapi import BooleanWidget
from Products.Archetypes.atapi import DateTimeField
from Products.Archetypes.atapi import CalendarWidget
from Products.Archetypes.atapi import BaseSchema
from Products.Archetypes.atapi import BaseContent
from Products.Archetypes.atapi import registerType
from Products.Archetypes.atapi import BooleanField

from Products.eXtremeManagement.interfaces import IXMBooking
from Products.eXtremeManagement.content.schemata import quarter_vocabulary
from Products.eXtremeManagement.content.schemata import hour_vocabulary

schema = Schema((
    IntegerField(
        name='hours',
        vocabulary=hour_vocabulary,
        validators=('isInt', ),
        default=0,
        widget=SelectionWidget(
            label='Hours',
            label_msgid='eXtremeManagement_label_hours',
            i18n_domain='eXtremeManagement'),
    ),
    IntegerField(
        name='minutes',
        vocabulary=quarter_vocabulary,
        validators=('isInt', ),
        default=0,
        widget=SelectionWidget(
            label='Minutes',
            label_msgid='eXtremeManagement_label_minutes',
            i18n_domain='eXtremeManagement'),
    ),
    BooleanField(
        name='billable',
        default_method='is_billable',
        widget=BooleanWidget(
            label='Billable',
            label_msgid='eXtremeManagement_label_billable',
            i18n_domain='eXtremeManagement')
    ),
    DateTimeField(
        name='bookingDate',
        required=1,
        default_method=DateTime,
        validators=('isValidDate', ),
        widget=CalendarWidget(
            show_hm=False,
            description="Date that you worked on this task",
            label='Bookingdate',
            label_msgid='eXtremeManagement_label_bookingDate',
            description_msgid='eXtremeManagement_help_bookingDate',
            i18n_domain='eXtremeManagement'),
    ),
), )

BaseSchema = BaseSchema.copy()
BaseSchema['id'].widget.visible = dict(edit=0, view=0)
BaseSchema['description'].isMetadata = False
BaseSchema['description'].schemata = 'default'
Booking_schema = BaseSchema + schema


class Booking(BaseContent):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (BaseContent.__implements__, )
    implements(IXMBooking)

    # This name appears in the 'add' box
    archetype_name = 'Booking'
    portal_type = meta_type = 'Booking'
    typeDescription = "Booking"
    typeDescMsgId = 'description_edit_booking'
    _at_rename_after_creation = True
    schema = Booking_schema

    @property
    def actual_time(self):
        return self.getHours() + (self.getMinutes() / 60.0)

    def is_billable(self):
        """ Get the default from the project setting. """
        return self.getBillableProject()

    security.declarePublic('recalc')

    def recalc(self):
        """See the IActualHours interface.
        With our implementation we only need a reindex here actually.
        """
        self.reindexObject(idxs=['actual_time'])

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


registerType(Booking, 'eXtremeManagement')
