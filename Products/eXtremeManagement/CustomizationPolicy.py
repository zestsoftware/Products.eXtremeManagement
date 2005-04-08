from Products.CMFPlone.Portal import addPolicy
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.Expression import Expression
from Products.CMFCore import CMFCorePermissions
from Products.CMFCore.DirectoryView import addDirectoryViews, registerDirectory
from Products.CMFPlone.CustomizationPolicy import DefaultCustomizationPolicy

class eXtremeManagementPolicy(DefaultCustomizationPolicy):
    """ Customize plone for eXtremeManagement """

    def customize(self, portal):
        # Install the Plone Site with the default policy and
        # update it with this one. All changes to standard
        # Plone will be done in this policy.



def register(context, app_state):
    addPolicy('eXtremeManagement', eXtremeManagementPolicy())
