from AccessControl import ClassSecurityInfo
from zope.interface import implements

from Products.Archetypes.atapi import *

from Products.eXtremeManagement.interfaces.IXMCustomer import IXMCustomer as IXMCustomerZope2
from Products.eXtremeManagement.config import *
from Products.eXtremeManagement.interfaces import IXMCustomer

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
            description="Enter address.",
            label='Address',
            label_msgid='eXtremeManagement_label_address',
            description_msgid='eXtremeManagement_help_address',
            i18n_domain='eXtremeManagement'),
    ),
    StringField(
        name='zipCode',
        required=1,
        widget=StringWidget(
            description="Enter zip code.",
            label='Zip code',
            label_msgid='eXtremeManagement_label_zipCode',
            description_msgid='eXtremeManagement_help_zipCode',
            i18n_domain='eXtremeManagement'),
    ),
    StringField(
        name='city',
        required=1,
        widget=StringWidget(
            description="Enter city name.",
            label='City',
            label_msgid='eXtremeManagement_label_city',
            description_msgid='eXtremeManagement_help_city',
            i18n_domain='eXtremeManagement'),
    ),
    StringField(
        name='country',
        required=1,
        widget=StringWidget(
            description="Enter country.",
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
            description="Enter your phone number.",
            label='Phone',
            label_msgid='eXtremeManagement_label_phone',
            description_msgid='eXtremeManagement_help_phone',
            i18n_domain='eXtremeManagement'),
    ),
    StringField(
        name='fax',
        widget=IntegerWidget(
            size="30",
            description="Enter your fax number.",
            label='Fax',
            label_msgid='eXtremeManagement_label_fax',
            description_msgid='eXtremeManagement_help_fax',
            i18n_domain='eXtremeManagement',)
    ),
    StringField(
        name='website',
        widget=StringWidget(
            description="Enter your website address.",
            label='Website',
            label_msgid='eXtremeManagement_label_website',
            description_msgid='eXtremeManagement_help_website',
            i18n_domain='eXtremeManagement')
    ),
),)

FolderSchema = OrderedBaseFolderSchema.copy()
FolderSchema['description'].isMetadata = False
FolderSchema['description'].schemata = 'default'
FolderSchema['id'].widget.visible = dict(edit=0, view=0)
Customer_schema = FolderSchema + schema


class Customer(OrderedBaseFolder):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (OrderedBaseFolder.__implements__, IXMCustomerZope2)
    implements(IXMCustomer)
    archetype_name = 'Customer'
    portal_type = meta_type = 'Customer'
    allowed_content_types = ['ProjectMember']
    filter_content_types = 1
    global_allow = 0
    content_icon = 'group_icon.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "Customer"
    typeDescMsgId = 'description_edit_customer'
    _at_rename_after_creation = True
    schema = Customer_schema

    actions =  ({'action': "string:${object_url}/folder_localrole_form",
                 'category': "object",
                 'id': 'local_roles',
                 'name': 'Sharing',
                 'permissions': ("View",),
                 'condition': 'python:1'},
    )

    # Methods from Interface IXMCustomer
    security.declarePublic('getName')
    def getName(self):
        """
        """
        pass

registerType(Customer, PROJECTNAME)
