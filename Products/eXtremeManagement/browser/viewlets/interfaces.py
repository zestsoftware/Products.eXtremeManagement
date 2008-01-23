import zope.schema
from zope.interface import directlyProvides
from zope.viewlet.interfaces import IViewletManager
from zope.contentprovider.interfaces import ITALNamespaceData


class ISimpleTaskList(IViewletManager):
    realtasks = zope.schema.Text(title=u'Text of the message box')


directlyProvides(ISimpleTaskList, ITALNamespaceData)
