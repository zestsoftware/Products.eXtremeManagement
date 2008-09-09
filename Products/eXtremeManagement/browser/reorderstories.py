from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from zope.cachedescriptors.property import Lazy
from plone.memoize.view import memoize
from zope.component import getMultiAdapter


from Products.eXtremeManagement.browser.xmbase import XMBaseView
from Products.eXtremeManagement.browser.projects import ProjectView
from Products.eXtremeManagement.utils import formatTime


class ReorderStoriesView(ProjectView):
    pass
