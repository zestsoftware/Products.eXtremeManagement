# File: CustomerFolder.py
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

BaseFolderSchema = OrderedBaseFolderSchema.copy()
BaseFolderSchema['description'].isMetadata = False
BaseFolderSchema['description'].schemata = 'default'

##/code-section module-header

schema=Schema((
),
)


##code-section after-schema #fill in your manual code here
##/code-section after-schema

class CustomerFolder(OrderedBaseFolder,BaseFolder):
    security = ClassSecurityInfo()
    __implements__ = (getattr(OrderedBaseFolder,'__implements__',()),) + (getattr(BaseFolder,'__implements__',()),)


    # This name appears in the 'add' box
    archetype_name             = 'CustomerFolder'

    meta_type                  = 'CustomerFolder' 
    portal_type                = 'CustomerFolder' 
    allowed_content_types      = ['Customer'] + list(getattr(OrderedBaseFolder, 'allowed_content_types', []))
    filter_content_types       = 1
    global_allow               = 1
    allow_discussion           = 0
    #content_icon               = 'CustomerFolder.gif'
    immediate_view             = 'base_view'
    default_view               = 'base_view'
    typeDescription            = "CustomerFolder"
    typeDescMsgId              = 'description_edit_customerfolder'

    schema = BaseFolderSchema + \
             getattr(OrderedBaseFolder,'schema',Schema(())) + \
             schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header


    #Methods

registerType(CustomerFolder,PROJECTNAME)
# end of class CustomerFolder

##code-section module-footer #fill in your manual code here
##/code-section module-footer



