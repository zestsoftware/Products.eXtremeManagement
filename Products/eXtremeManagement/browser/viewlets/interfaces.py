import zope.schema
from zope.interface import directlyProvides
from zope.viewlet.interfaces import IViewletManager
from zope.contentprovider.interfaces import ITALNamespaceData


class ISimpleTaskList(IViewletManager):
    realtasks = zope.schema.Text(title=u'Text of the message box')
    show_story = zope.schema.Bool(title=u'Show a column for the story.')

directlyProvides(ISimpleTaskList, ITALNamespaceData)
