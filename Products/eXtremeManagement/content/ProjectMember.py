# File: ProjectMember.py
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
    StringField('fullname',
        index="FieldIndex",
        widget=StringWidget(
            description="Enter a name, eg. John Smith.",
            label='Fullname',
            label_msgid='eXtremeManagement_label_fullname',
            description_msgid='eXtremeManagement_help_fullname',
            i18n_domain='eXtremeManagement',
        ),
        required=1
    ),

    StringField('phone',
        index="FieldIndex",
        widget=IntegerWidget
        (
            size="30",
            description="Enter your phone number.",
            label='Phone',
            label_msgid='eXtremeManagement_label_phone',
            description_msgid='eXtremeManagement_help_phone',
            i18n_domain='eXtremeManagement',
        ),
        required=1
    ),

    StringField('email',
        index="FieldIndex",
        widget=StringWidget(
            description="Enter your email address.",
            label='Email',
            label_msgid='eXtremeManagement_label_email',
            description_msgid='eXtremeManagement_help_email',
            i18n_domain='eXtremeManagement',
        )
    ),

),
)


##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

ProjectMember_schema = BaseSchema + \
    schema

##code-section after-schema #fill in your manual code here
ProjectMember_schema = schema + BaseSchema
##/code-section after-schema

class ProjectMember(BaseContent):
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseContent,'__implements__',()),)


    # This name appears in the 'add' box
    archetype_name             = 'ProjectMember'

    meta_type                  = 'ProjectMember'
    portal_type                = 'ProjectMember'
    allowed_content_types      = []
    filter_content_types       = 0
    global_allow               = 0
    allow_discussion           = 0
    content_icon               = 'user.gif'
    immediate_view             = 'base_view'
    default_view               = 'base_view'
    suppl_views                = ()
    typeDescription            = "ProjectMember"
    typeDescMsgId              = 'description_edit_projectmember'

    _at_rename_after_creation  = True

    schema = ProjectMember_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header


    #Methods

registerType(ProjectMember,PROJECTNAME)
# end of class ProjectMember

##code-section module-footer #fill in your manual code here
##/code-section module-footer



