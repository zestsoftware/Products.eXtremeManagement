from zope.interface import implements
from AccessControl import ClassSecurityInfo

from Products.Archetypes.atapi import BooleanField
from Products.Archetypes.atapi import BooleanWidget
from Products.Archetypes.atapi import CalendarWidget
from Products.Archetypes.atapi import DateTimeField
from Products.Archetypes.atapi import OrderedBaseFolder
from Products.Archetypes.atapi import OrderedBaseFolderSchema
from Products.Archetypes.atapi import registerType
from Products.Archetypes.atapi import Schema

from Products.eXtremeManagement.interfaces import IXMOffer

schema = Schema((
    DateTimeField(
        name='startDate',
        validators=('isValidDate', ),
        widget=CalendarWidget(
            show_hm=False,
            label='Start date',
            label_msgid='eXtremeManagement_label_startDate',
            i18n_domain='eXtremeManagement'),
    ),
    DateTimeField(
        name='endDate',
        validators=('isValidDate', ),
        widget=CalendarWidget(
            show_hm=False,
            label='End date',
            label_msgid='eXtremeManagement_label_endDate',
            i18n_domain='eXtremeManagement'),
    ),
    BooleanField(
        name='show_draft',
        default="False",
        widget=BooleanWidget(
            label='Show draft state',
            label_msgid='eXtremeManagement_label_show_draft',
            description='Check this to have the Offer view '
                        'mark stories which are still in the draft state',
            description_msgid='eXtremeManagement_help_show_draft',
            i18n_domain='eXtremeManagement'),
    ),
), )

FolderSchema = OrderedBaseFolderSchema.copy()
FolderSchema['description'].isMetadata = False
FolderSchema['description'].schemata = 'default'
Offer_schema = FolderSchema + schema

UNACCEPTABLE_STATUSES = ['draft', 'pending']


class Offer(OrderedBaseFolder):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (OrderedBaseFolder.__implements__, )
    implements(IXMOffer)

    # This name appears in the 'add' box
    archetype_name = 'Offer'
    portal_type = meta_type = 'Offer'
    typeDescription = "Offer"
    typeDescMsgId = 'description_edit_offer'
    _at_rename_after_creation = True
    schema = Offer_schema

registerType(Offer, 'eXtremeManagement')
