import zope.schema
from zope.interface import directlyProvides
from zope.viewlet.interfaces import IViewletManager
from zope.contentprovider.interfaces import ITALNamespaceData


class ISimpleTaskList(IViewletManager):
    realtasks = zope.schema.Text(
        title=u'Alternative for tasks that might be in the view.')
    show_story = zope.schema.Bool(title=u'Show a column for the story.')

directlyProvides(ISimpleTaskList, ITALNamespaceData)


class ISimpleStoryList(IViewletManager):
    realstories = zope.schema.Text(
        title=u'Alternative for stories that might be in the view.')
    iteration_object = zope.schema.Text(
        title=u'The iteration object or None.')
    iteration_dict = zope.schema.Text(
        title=u'A dictionary for the iteration, from the @@iteration view.')
    iteration_number = zope.schema.TextLine(
        title=u'Number (as string) of the iteration.')

    show_iteration = zope.schema.Bool(title=u'Show a row for the iteration.')
    show_progress = zope.schema.Bool(title=u'Show progress bar per story.')
    show_totals = zope.schema.Bool(title=u'Show totals for the iteration.')

directlyProvides(ISimpleStoryList, ITALNamespaceData)


class IStoryDetails(IViewletManager):
    realtasks = zope.schema.Text(
        title=u'Alternative for tasks that might be in the view.')
    story_object = zope.schema.Bool(
        title=u'Story object whose details should be rendered.')
    number_of_comments = zope.schema.Int(
        title=u'Number of comments added to this Story.')

directlyProvides(IStoryDetails, ITALNamespaceData)


class IStoryDetailsBox(IViewletManager):
    story_object = zope.schema.Bool(
        title=u'Story object whose details should be rendered.')


directlyProvides(IStoryDetailsBox, ITALNamespaceData)
