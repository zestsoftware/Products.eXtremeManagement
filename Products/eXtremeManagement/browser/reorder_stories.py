import logging

#from zope.cachedescriptors.property import Lazy
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from kss.core import kssaction
from plone.app.kss.plonekssview import PloneKSSView

from Products.eXtremeManagement.browser.projects import ProjectView
from Products.eXtremeManagement import XMMessageFactory as _
#from Products.eXtremeManagement.utils import formatTime

logger = logging.getLogger('movestory')


class ReorderStoriesView(ProjectView):
    """Browser view for reordering stories.

    We set up the view:

      >>> view = ReorderStoriesView(context=None, request=None)

    view.iterations() gives us the current and the open iterations.

      >>> view.current_iterations = lambda: [1, 2] # Mock
      >>> view.open_iterations = lambda: [3, 4] # Mock
      >>> view.iterations()
      [1, 2, 3, 4]

    The iterations are returned (from a brain) as a dict, including a list of
    stories.

      >>> class MockBrain(object):
      ...     def __init__(self, **kw):
      ...         self.kw = kw
      ...     def __getattr__(self, key):
      ...         return self.kw[key]
      >>> class MockIterationView(object):
      ...     def __init__(self, context, request):
      ...         pass
      ...     def stories(self):
      ...         return 'list of stories'
      >>> import zope.component
      >>> from zope.interface import Interface
      >>> from Products.eXtremeManagement.browser.interfaces import IIterationView
      >>> zope.component.provideAdapter(factory=MockIterationView,
      ...                               adapts=(None, None),
      ...                               provides=IIterationView,
      ...                               name=u'iteration')


      >>> brain = MockBrain(Title='title', Description='desc',
      ...                   getObject=lambda: None, UID='1234')
      >>> from pprint import pprint
      >>> result = view.iterationbrain2dict(brain)
      >>> pprint(result)
      {'brain': <Products.eXtremeManagement.browser.reorder_stories.MockBrain ...>,
       'description': 'desc',
       'stories': 'list of stories',
       'title': 'title',
       'uid': '1234'}

    """

    def iterations(self):
        return self.current_iterations() + self.open_iterations()

    def iterationbrain2dict(self, brain):
        """Get a dict with info from this iteration brain.

        This one gets used by current_iterations() and open_iterations().
        """
        #estimate = brain.estimate
        #actual = brain.actual_time
        iteration = brain.getObject()
        iteration_view = getMultiAdapter((iteration, self.request),
                                         name='iteration')
        stories = iteration_view.stories()
        returnvalue = dict(
            #url = brain.getURL(),
            title = brain.Title,
            description = brain.Description,
            #man_hours = brain.getManHours,
            #estimate = formatTime(estimate),
            #actual = formatTime(actual),
            #difference = formatTime(estimate - actual),
            brain = brain,
            stories = stories,
            uid = brain.UID,
        )
        return returnvalue


class MoveStory(PloneKSSView):
    """React on kss drag/drop of story to another iteration.

    Some setup

      >>> class MockContext(object):
      ...     pass
      >>> class MockUidCatalog(object):
      ...     uids = {}
      ...     def __call__(self, UID=None):
      ...         if UID in self.uids:
      ...             return [self.uids[UID]]
      ...         else:
      ...             return []
      >>> class MockBrainObject(object):
      ...     def __init__(self, **kw):
      ...         self.dict = kw
      ...     def getObject(self):
      ...         return self
      ...     def __repr__(self):
      ...         return '<brain/object %s>' % self.dict.get('title')
      >>> context = MockContext()
      >>> context.uid_catalog = MockUidCatalog()
      >>> view = MoveStory(context, None)

    The UIDs passed to kss get converted into their respective objects. A
    wrong UID is caught.

      >>> context.uid_catalog.uids = {'1': MockBrainObject(title='1'),
      ...                             '2': MockBrainObject(title='2'),
      ...                             '3': MockBrainObject(title='3')}
      >>> view.extract_objects('1', '2', '3')
      (<brain/object 1>, <brain/object 2>, <brain/object 3>)
      >>> view.extract_objects('1', '2', 'non-existing')
      (None, None, None)

    """

    @kssaction
    def move_story(self, source_id, target_id, story_id, index):
        plone = self.getCommandSet('plone')
        source, target, story = self.extract_objects(source_id,
                                                     target_id,
                                                     story_id)
        if source == None: # The rest is also None.
            plone.issuePortalMessage(_(u'Drag/drop uids incorrect'),
                                     msgtype='error')
            return
        logger.info('%s dragged from %s to %s', story, source, target)
        # Check if it is a different iteration.
        # Cut/paste.

    def extract_objects(self, source_id, target_id, story_id):
        uid_catalog = getToolByName(self.context, 'uid_catalog')
        try:
            brain = uid_catalog(UID=source_id)[0]
            source = brain.getObject()
            brain = uid_catalog(UID=target_id)[0]
            target = brain.getObject()
            brain = uid_catalog(UID=story_id)[0]
            story = brain.getObject()
            return (source, target, story)
        except IndexError:
            return (None, None, None)
