# eXtremeManagement Module
__author__  = 'Ahmad Hadi'
__docformat__ = 'restructuredtext'

import sys
from Globals import package_home
from Products.CMFCore.utils import ContentInit
from Products.CMFCore import utils as cmf_utils
from Products.CMFCore.DirectoryView import registerDirectory
from Products.Archetypes import public as atapi
from Products.Archetypes.public import process_types, listTypes
import os, os.path

from Products.eXtremeManagement.config import *
from Products.eXtremeManagement import CustomizationPolicy
from Products.eXtremeManagement import eXtremeManagement
from Products.eXtremeManagement.permissions import *
import config, permissions

registerDirectory(SKINS_DIR, GLOBALS)

#def initialize(context):
#    CustomizationPolicy.register(context, globals())
#    listOfTypes = listTypes(PROJECTNAME)
#    content_types, constructors, ftis = process_types(
#        listOfTypes,
#        PROJECTNAME)
#
#    ContentInit(
#        PROJECTNAME + ' Content',
#        content_types      = content_types,
#        permission         = ADD_CONTENT_PERMISSION,
#        extra_constructors = constructors,
#        fti                = ftis,
#        ).initialize(context)

import utils

def initialize(context):
    extreme_types = atapi.listTypes(config.PROJECTNAME)
    content_types, constructors, ftis = atapi.process_types( extreme_types,
                                                             config.PROJECTNAME)
    # separate out the content types so we can register them in groups
    # based on permissions

    type_map = utils.separateTypesByPerm(
        extreme_types,
        content_types,
        constructors,
        permissions.ContentPermissionMap
        )

    for permission in type_map:
        factory_info = type_map[ permission ]
        content_types = tuple([fi[0] for fi in factory_info])
        constructors  = tuple([fi[1] for fi in factory_info])

        cmf_utils.ContentInit(
            config.PROJECTNAME + ' Content',
            content_types      = content_types,
            permission         = permission,
            extra_constructors = constructors,
            fti                = ftis,
            ).initialize(context)


