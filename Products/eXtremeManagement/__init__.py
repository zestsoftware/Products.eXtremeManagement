# -*- coding: utf-8 -*-
#
# File: eXtremeManagement.py
#
# Copyright (c) 2006 by Zest software, Lovely Systems
# Generator: ArchGenXML Version 1.5.1-svn
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

__author__ = """Ahmad Hadi <a.hadi@zestsoftware.nl>, Maurits van Rees
<m.van.rees@zestsoftware.nl>, Jodok Batlogg <jodok.batlogg@lovelysystems.com>"""
__docformat__ = 'plaintext'


# There are three ways to inject custom code here:
#
#   - To set global configuration variables, create a file AppConfig.py.
#       This will be imported in config.py, which in turn is imported in
#       each generated class and in this file.
#   - To perform custom initialisation after types have been registered,
#       use the protected code section at the bottom of initialize().
#   - To register a customisation policy, create a file CustomizationPolicy.py
#       with a method register(context) to register the policy.

from zLOG import LOG, INFO, DEBUG

LOG('eXtremeManagement', DEBUG, 'Installing Product')

try:
    import CustomizationPolicy
except ImportError:
    CustomizationPolicy = None

import os, os.path

from Globals import package_home
from Products.CMFCore import utils as cmfutils
from Products.CMFCore import CMFCorePermissions
from Products.CMFCore import DirectoryView
from Products.GenericSetup import EXTENSION
from Products.GenericSetup import profile_registry
from Products.CMFPlone.utils import ToolInit
import Products.CMFPlone.interfaces
from Products.Archetypes.atapi import *
from Products.Archetypes import listTypes
from Products.Archetypes.utils import capitalize

from Products.eXtremeManagement.config import *

DirectoryView.registerDirectory('skins', product_globals)
DirectoryView.registerDirectory('skins/eXtremeManagement',
                                    product_globals)

def initialize(context):
    # imports packages and types for registration
    import content
    import tools
    import interfaces

    # Initialize portal tools
    tools = [tools.eXtremeManagementTool.eXtremeManagementTool]
    ToolInit( PROJECTNAME +' Tools',
                tools = tools,
                icon='tool.gif'
                ).initialize( context )

    # Initialize portal content
    all_content_types, all_constructors, all_ftis = process_types(
        listTypes(PROJECTNAME),
        PROJECTNAME)

    cmfutils.ContentInit(
        PROJECTNAME + ' Content',
        content_types      = all_content_types,
        permission         = DEFAULT_ADD_CONTENT_PERMISSION,
        extra_constructors = all_constructors,
        fti                = all_ftis,
        ).initialize(context)

    # Give it some extra permissions to control them on a per class limit
    for i in range(0,len(all_content_types)):
        klassname=all_content_types[i].__name__
        if not klassname in ADD_CONTENT_PERMISSIONS:
            continue

        context.registerClass(meta_type   = all_ftis[i]['meta_type'],
                              constructors= (all_constructors[i],),
                              permission  = ADD_CONTENT_PERMISSIONS[klassname])

    # Register generic setup profile
    profile_registry.registerProfile(
        name='default',
        title='Extreme Management',
        description='Profile for Extreme Management',
        path='profiles/default',
        product='preusetup',
        profile_type=EXTENSION,
        for_=Products.CMFPlone.interfaces.IPloneSiteRoot)
