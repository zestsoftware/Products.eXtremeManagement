import os.path
import sys
from StringIO import StringIO
from sets import Set
import transaction
from App.Common import package_home
from zExceptions import NotFound, BadRequest
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.utils import manage_addTool
from Products.ExternalMethod.ExternalMethod import ExternalMethod

from Products.Archetypes.Extensions.utils import installTypes
from Products.Archetypes.Extensions.utils import install_subskin
from Products.Archetypes.config import TOOL_NAME as ARCHETYPETOOLNAME
from Products.Archetypes.atapi import listTypes
from Products.eXtremeManagement.config import PROJECTNAME
from Products.eXtremeManagement.config import product_globals as GLOBALS

def install(self, reinstall=False):
    """ External Method to install eXtremeManagement """
    out = StringIO()
    print >> out, "Installation log of %s:" % PROJECTNAME

    # If the config contains a list of dependencies, try to install
    # them.  Add a list called DEPENDENCIES to your custom
    # AppConfig.py (imported by config.py) to use it.
    try:
        from Products.eXtremeManagement.config import DEPENDENCIES
    except:
        DEPENDENCIES = []
    portal = getToolByName(self,'portal_url').getPortalObject()
    quickinstaller = portal.portal_quickinstaller
    for dependency in DEPENDENCIES:
        print >> out, "Installing dependency %s:" % dependency
        quickinstaller.installProduct(dependency)
        transaction.commit(1)

    classes = listTypes(PROJECTNAME)
    installTypes(self, out,
                 classes,
                 PROJECTNAME)
    install_subskin(self, out, GLOBALS)


    # try to call a custom install method
    # in 'AppInstall.py' method 'install'
    try:
        install = ExternalMethod('temp', 'temp',
                                 PROJECTNAME+'.AppInstall', 'install')
    except NotFound:
        install = None

    if install:
        print >>out,'Custom Install:'
        try:
            res = install(self, reinstall)
        except TypeError:
            res = install(self)
        if res:
            print >>out,res
        else:
            print >>out,'no output'
    else:
        print >>out,'no custom install'

    return out.getvalue()

def uninstall(self, reinstall=False):
    out = StringIO()

    # unhide tools in the search form
    portalProperties = getToolByName(self, 'portal_properties', None)
    if portalProperties is not None:
        siteProperties = getattr(portalProperties, 'site_properties', None)
        if siteProperties is not None and siteProperties.hasProperty('types_not_searched'):
            for tool in ['eXtremeManagementTool']:
                current = list(siteProperties.getProperty('types_not_searched'))
                if tool in current:
                    current.remove(tool)
                    siteProperties.manage_changeProperties(**{'types_not_searched' : current})

    # unhide tools
    portalProperties = getToolByName(self, 'portal_properties', None)
    if portalProperties is not None:
        navtreeProperties = getattr(portalProperties, 'navtree_properties', None)
        if navtreeProperties is not None and navtreeProperties.hasProperty('idsNotToList'):
            for toolname in ['xm_tool']:
                current = list(navtreeProperties.getProperty('idsNotToList'))
                if toolname in current:
                    current.remove(toolname)
                    navtreeProperties.manage_changeProperties(**{'idsNotToList' : current})

    # try to call a custom uninstall method
    # in 'AppInstall.py' method 'uninstall'
    try:
        uninstall = ExternalMethod('temp', 'temp',
                                   PROJECTNAME+'.AppInstall', 'uninstall')
    except:
        uninstall = None

    if uninstall:
        print >>out,'Custom Uninstall:'
        try:
            res = uninstall(self, reinstall)
        except TypeError:
            res = uninstall(self)
        if res:
            print >>out,res
        else:
            print >>out,'no output'
    else:
        print >>out,'no custom uninstall'

    return out.getvalue()
