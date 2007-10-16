from StringIO import StringIO
from sets import Set
from Products.CMFCore.utils import getToolByName
from Products.eXtremeManagement.config import *


def applyGenericSetupProfile(portal, out):
    setup_tool = getToolByName(portal, 'portal_setup')
    setup_tool.setImportContext('profile-eXtremeManagement:default')
    print >> out, "Applying the generic setup profile for eXtremeManagement..."
    setup_tool.runAllImportSteps(purge_old=False)
    setup_tool.setImportContext('profile-Products.CMFPlone:plone')
    print >> out, "Applied the generic setup profile for eXtremeManagement"


def install(self):
    out = StringIO()
    print >> out, "Apply the generic setup profile"
    applyGenericSetupProfile(self, out)
    out.write("Successfully installed %s.\n" % PROJECTNAME)

    return out.getvalue()
