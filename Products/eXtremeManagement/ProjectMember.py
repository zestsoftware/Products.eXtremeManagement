# File: ProjectMember.py
# 
# Copyright (c) 2005 by Zest software 2005
# Generator: ArchGenXML Version 1.4.0-beta2 http://sf.net/projects/archetypes/
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

##/code-section module-header

schema=Schema((
    StringField('fullname',
        index="FieldIndex",
        widget=StringWidget(
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
            label='Phone',
            label_msgid='eXtremeManagement_label_phone',
            description_msgid='eXtremeManagement_help_phone',
            i18n_domain='eXtremeManagement',
        ),
        required=1,
        size="30"
    ),
    
    StringField('email',
        index="FieldIndex",
        widget=StringWidget(
            label='Email',
            label_msgid='eXtremeManagement_label_email',
            description_msgid='eXtremeManagement_help_email',
            i18n_domain='eXtremeManagement',
        )
    ),
    
    TextField('comments',
        widget=TextAreaWidget(
            label='Comments',
            label_msgid='eXtremeManagement_label_comments',
            description_msgid='eXtremeManagement_help_comments',
            i18n_domain='eXtremeManagement',
        )
    ),
    
),
)


##code-section after-schema #fill in your manual code here
##/code-section after-schema

class ProjectMember(BaseContent,BaseContent):
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseContent,'__implements__',()),) + (getattr(BaseContent,'__implements__',()),)


    # This name appears in the 'add' box
    archetype_name             = 'ProjectMember'

    meta_type                  = 'ProjectMember' 
    portal_type                = 'ProjectMember' 
    allowed_content_types      = [] + list(getattr(BaseContent, 'allowed_content_types', []))
    filter_content_types       = 0
    global_allow               = 0
    allow_discussion           = 0
    #content_icon               = 'ProjectMember.gif'
    immediate_view             = 'base_view'
    default_view               = 'base_view'
    typeDescription            = "ProjectMember"
    typeDescMsgId              = 'description_edit_projectmember'

    schema = BaseSchema + \
             getattr(BaseContent,'schema',Schema(())) + \
             schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header


    #Methods

registerType(ProjectMember,PROJECTNAME)
# end of class ProjectMember

##code-section module-footer #fill in your manual code here
##/code-section module-footer



