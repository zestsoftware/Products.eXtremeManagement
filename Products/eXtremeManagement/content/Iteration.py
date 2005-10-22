# File: Iteration.py
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

#OrderedBaseFolderSchema = OrderedBaseFolderSchema.copy()
#OrderedBaseFolderSchema['description'].isMetadata = False
#OrderedBaseFolderSchema['description'].schemata = 'default'
#OrderedBaseFolderSchema['id'].widget.visible = {'edit':'hidden', 'view':'invisible'

##/code-section module-header

schema=Schema((
),
)


##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Iteration_schema = OrderedBaseFolderSchema + \
    schema

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Iteration(OrderedBaseFolder):
    security = ClassSecurityInfo()
    __implements__ = (getattr(OrderedBaseFolder,'__implements__',()),)


    # This name appears in the 'add' box
    archetype_name             = 'Iteration'

    meta_type                  = 'Iteration'
    portal_type                = 'Iteration'
    allowed_content_types      = ['Story']
    filter_content_types       = 1
    global_allow               = 0
    allow_discussion           = 0
    content_icon               = 'iteration_icon.gif'
    immediate_view             = 'base_view'
    default_view               = 'base_view'
    suppl_views                = ()
    typeDescription            = "Iteration"
    typeDescMsgId              = 'description_edit_iteration'

    _at_rename_after_creation  = True

    schema = Iteration_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header


    #Methods

registerType(Iteration,PROJECTNAME)
# end of class Iteration

##code-section module-footer #fill in your manual code here
##/code-section module-footer



