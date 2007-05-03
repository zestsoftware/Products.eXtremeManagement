from zope.interface import implements
from AccessControl import ClassSecurityInfo

from Products.Archetypes.atapi import *

from Products.eXtremeManagement.config import *
from Products.eXtremeManagement.interfaces import IXMProjectMember

schema = Schema((
    StringField(
        name='fullname',
        index="FieldIndex",
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
        index="FieldIndex",
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
        index="FieldIndex",
        widget=StringWidget(
            description="Enter your email address.",
            label='Email',
            label_msgid='eXtremeManagement_label_email',
            description_msgid='eXtremeManagement_help_email',
            i18n_domain='eXtremeManagement')
    ),
),)

BaseSchema = BaseSchema.copy()
BaseSchema['id'].widget.visible = dict(edit=0, view=0)
ProjectMember_schema = BaseSchema + schema


class ProjectMember(BaseContent):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (BaseContent.__implements__,)
    implements(IXMProjectMember)

    # This name appears in the 'add' box
    archetype_name = 'Project Member'
    portal_type = meta_type = 'ProjectMember'
    allowed_content_types = []
    filter_content_types = 0
    global_allow = 0
    content_icon = 'user.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "ProjectMember"
    typeDescMsgId = 'description_edit_projectmember'
    _at_rename_after_creation = True
    schema = ProjectMember_schema

registerType(ProjectMember, PROJECTNAME)
