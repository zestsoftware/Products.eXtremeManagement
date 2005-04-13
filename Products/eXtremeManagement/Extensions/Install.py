# AUTHORS: Ahmad Hadi

from Products.Archetypes.public import listTypes
from Products.Archetypes.Extensions.utils import installTypes, install_subskin
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.CMFCorePermissions import ManagePortal
from StringIO import StringIO

from Products.eXtremeManagement.config import PROJECTNAME, GLOBALS
from Products.eXtremeManagement.config import *

def setupProps(portal):
    # Add eXtreme Props
    if not hasattr(portal.portal_properties, 'extreme_properties'):
        portal.portal_properties.addPropertySheet('extreme_properties', 'eXtreme Properties')
        props = portal.portal_properties.extreme_properties
        props._setProperty('hours', ['01', '02', '03', '04', '05', '06', '07', 
                                     '08', '09', '10', '11', '12', '13', '14', '15'], 'lines')
        props._setProperty('minutes', ['0', '15', '30', '45'], 'lines')


def setupSkin(portal):
    # Set up the skins
    _dirs = ( 'eXtremeManagement', )
    sk_tool = getToolByName(portal, 'portal_skins')
    path=[elem.strip() for elem in sk_tool.getSkinPath('Plone Default').split(',')]

    for d in _dirs:
        try: path.insert(path.index('custom')+1, d)
        except ValueError: path.append(d)

    path=','.join(path)
    sk_tool.addSkinSelection('eXtremeManagement', path)
    if not 'eXtremeManagement' in  portal.portal_skins.objectIds():
        addDirectoryViews(sk_tool, 'skins', globals())
    # set default skin
    sk_tool.default_skin = 'eXtremeManagement'


def install(self):
    out = StringIO()
    installTypes(self, out,
                 listTypes(PROJECTNAME),
                 PROJECTNAME)

    install_subskin(self, out, GLOBALS)

    out.write("Successfully installed %s." % PROJECTNAME)
   
    print >> out, "Adding eXtreme properties"
    setupProps(self)

    print >> out, "Customize the portal"
    setupSkin(self)

    return out.getvalue()


def uninstall(self):
    out = StringIO()

    return out.getvalue()
 
