# eXtremeManagement Module
__author__  = 'Ahmad Hadi'
__docformat__ = 'restructuredtext'

import sys
from Globals import package_home
from Products.CMFCore.utils import ContentInit
from Products.CMFCore.DirectoryView import registerDirectory
import os, os.path

from Products.eXtremeManagement.config import *
#from Products.eXtremeManagement import CustomizationPolicy

registerDirectory(SKINS_DIR, GLOBALS)

def initialize(context):
    #CustomizationPolicy.register(context, globals())
    listOfTypes = listTypes(PROJECTNAME)
    content_types, constructors, ftis = process_types(
        listOfTypes,
        PROJECTNAME)

    ContentInit(
        PROJECTNAME + ' Content',
        content_types      = content_types,
        permission         = ADD_CONTENT_PERMISSION,
        extra_constructors = constructors,
        fti                = ftis,
        ).initialize(context)

