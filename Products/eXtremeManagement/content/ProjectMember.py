from zope.interface import implements
from AccessControl import ClassSecurityInfo

from Products.Archetypes.atapi import BaseContent
from Products.Archetypes.atapi import BaseSchema
from Products.Archetypes.atapi import IntegerWidget
from Products.Archetypes.atapi import registerType
from Products.Archetypes.atapi import Schema
from Products.Archetypes.atapi import StringField
from Products.Archetypes.atapi import StringWidget

from Products.eXtremeManagement.interfaces import IXMProjectMember

# BBB Can be removed in release 2.1

schema = Schema((
    StringField(
        name='fullname',
        required=1,
        widget=StringWidget(
            description="Enter a name, eg. John Smith.",
            label='Full name',
            label_msgid='eXtremeManagement_label_fullname',
            description_msgid='eXtremeManagement_help_fullname',
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
        name='email',
        widget=StringWidget(
            description="Enter your email address.",
            label='Email',
            label_msgid='eXtremeManagement_label_email',
            description_msgid='eXtremeManagement_help_email',
            i18n_domain='eXtremeManagement')
    ),
), )

BaseSchema = BaseSchema.copy()
BaseSchema['id'].widget.visible = dict(edit=0, view=0)
ProjectMember_schema = BaseSchema + schema


class ProjectMember(BaseContent):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (BaseContent.__implements__, )
    implements(IXMProjectMember)

    # This name appears in the 'add' box
    archetype_name = 'Project Member'
    portal_type = meta_type = 'ProjectMember'
    typeDescription = "ProjectMember"
    typeDescMsgId = 'description_edit_projectmember'
    _at_rename_after_creation = True
    schema = ProjectMember_schema

registerType(ProjectMember, 'eXtremeManagement')
