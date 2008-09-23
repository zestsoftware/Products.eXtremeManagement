from AccessControl import ClassSecurityInfo
from zope.interface import implements

from Products.Archetypes.atapi import IntegerWidget
from Products.Archetypes.atapi import OrderedBaseFolder
from Products.Archetypes.atapi import OrderedBaseFolderSchema
from Products.Archetypes.atapi import registerType
from Products.Archetypes.atapi import Schema
from Products.Archetypes.atapi import StringField
from Products.Archetypes.atapi import StringWidget

from Products.eXtremeManagement.interfaces import IXMCustomer

# BBB Can be removed in release 2.1

schema = Schema((
    StringField(
        name='name',
        required=1,
        widget=StringWidget(
            description="Enter the company name for this customer",
            label='Name',
            label_msgid='eXtremeManagement_label_name',
            description_msgid='eXtremeManagement_help_name',
            i18n_domain='eXtremeManagement'),
    ),
    StringField(
        name='address',
        required=1,
        widget=StringWidget(
            label='Address',
            label_msgid='eXtremeManagement_label_address',
            description_msgid='eXtremeManagement_help_address',
            i18n_domain='eXtremeManagement'),
    ),
    StringField(
        name='zipCode',
        required=1,
        widget=StringWidget(
            label='Zip code',
            label_msgid='eXtremeManagement_label_zipCode',
            description_msgid='eXtremeManagement_help_zipCode',
            i18n_domain='eXtremeManagement'),
    ),
    StringField(
        name='city',
        required=1,
        widget=StringWidget(
            label='City',
            label_msgid='eXtremeManagement_label_city',
            description_msgid='eXtremeManagement_help_city',
            i18n_domain='eXtremeManagement'),
    ),
    StringField(
        name='country',
        required=1,
        widget=StringWidget(
            label='Country',
            label_msgid='eXtremeManagement_label_country',
            description_msgid='eXtremeManagement_help_country',
            i18n_domain='eXtremeManagement'),
    ),
    StringField(
        name='phone',
        required=1,
        widget=IntegerWidget(
            size="30",
            label='Phone',
            label_msgid='eXtremeManagement_label_phone',
            description_msgid='eXtremeManagement_help_phone',
            i18n_domain='eXtremeManagement'),
    ),
    StringField(
        name='fax',
        widget=IntegerWidget(
            size="30",
            label='Fax',
            label_msgid='eXtremeManagement_label_fax',
            description_msgid='eXtremeManagement_help_fax',
            i18n_domain='eXtremeManagement')
    ),
    StringField(
        name='website',
        widget=StringWidget(
            label='Website',
            label_msgid='eXtremeManagement_label_website',
            description_msgid='eXtremeManagement_help_website',
            i18n_domain='eXtremeManagement')
    ),
), )

FolderSchema = OrderedBaseFolderSchema.copy()
FolderSchema['description'].isMetadata = False
FolderSchema['description'].schemata = 'default'
FolderSchema['id'].widget.visible = dict(edit=0, view=0)
Customer_schema = FolderSchema + schema


class Customer(OrderedBaseFolder):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (OrderedBaseFolder.__implements__, )
    implements(IXMCustomer)
    archetype_name = 'Customer'
    portal_type = meta_type = 'Customer'
    typeDescription = "Customer"
    typeDescMsgId = 'description_edit_customer'
    _at_rename_after_creation = True
    schema = Customer_schema

    # Methods from Interface IXMCustomer
    security.declarePublic('getName')

    def getName(self):
        """
        """
        pass

registerType(Customer, 'eXtremeManagement')
