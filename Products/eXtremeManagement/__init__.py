from zLOG import LOG, INFO, DEBUG
LOG('eXtremeManagement', DEBUG, 'Installing Product')

import os, os.path

from Globals import package_home
from Products.CMFCore import utils as cmfutils
from Products.CMFCore import DirectoryView
import Products.CMFPlone.interfaces
from Products.Archetypes.atapi import *
from Products.Archetypes import listTypes
from Products.Archetypes.utils import capitalize

from Products.eXtremeManagement.config import *

# importing 'timing' sets up some interfaces.
from Products.eXtremeManagement import timing

DirectoryView.registerDirectory('skins', product_globals)
DirectoryView.registerDirectory('skins/eXtremeManagement',
                                    product_globals)

def initialize(context):
    # imports packages and types for registration
    import content
    import interfaces

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

    if HAS_GENERIC_SETUP:
        # Register generic setup profile
        from Products.GenericSetup import EXTENSION
        from Products.GenericSetup import profile_registry
        profile_registry.registerProfile(
            name='default',
            title='Extreme Management',
            description='Profile for Extreme Management',
            path='profiles/default',
            product='eXtremeManagement',
            profile_type=EXTENSION,
            for_=Products.CMFPlone.interfaces.IPloneSiteRoot)
