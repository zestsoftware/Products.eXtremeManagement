from zLOG import LOG, DEBUG
LOG('eXtremeManagement', DEBUG, 'Installing Product')

from Products.CMFCore import utils as cmfutils
from Products.CMFCore import DirectoryView
from Products.Archetypes.atapi import process_types
from Products.Archetypes import listTypes

from Products.eXtremeManagement import config

# importing 'timing' sets up some interfaces.
from Products.eXtremeManagement import timing

DirectoryView.registerDirectory('skins', config.product_globals)
DirectoryView.registerDirectory('skins/eXtremeManagement',
                                config.product_globals)

def initialize(context):
    # imports packages and types for registration
    import content
    import interfaces

    # Initialize portal content
    all_content_types, all_constructors, all_ftis = process_types(
        listTypes(config.PROJECTNAME),
        config.PROJECTNAME)

    cmfutils.ContentInit(
        config.PROJECTNAME + ' Content',
        content_types      = all_content_types,
        permission         = config.DEFAULT_ADD_CONTENT_PERMISSION,
        extra_constructors = all_constructors,
        fti                = all_ftis,
        ).initialize(context)

    # Give it some extra permissions to control them on a per class limit
    for i in range(0,len(all_content_types)):
        klassname=all_content_types[i].__name__
        if not klassname in config.ADD_CONTENT_PERMISSIONS:
            continue

        context.registerClass(
            meta_type   = all_ftis[i]['meta_type'],
            constructors= (all_constructors[i],),
            permission  = config.ADD_CONTENT_PERMISSIONS[klassname])
