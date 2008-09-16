"""View for listing iterations and stories and KSS for reordering them.

Unittests are in this file, functional and browser tests are in
../doc/reorder_stories.txt.

"""

import logging

#from zope.cachedescriptors.property import Lazy
from zope.component import getMultiAdapter
from zope.i18nmessageid import Message
from Products.CMFCore.utils import getToolByName
from kss.core import kssaction
from plone.app.kss.plonekssview import PloneKSSView

from Products.eXtremeManagement.browser.projects import ProjectView
from Products.eXtremeManagement import XMMessageFactory as _
#from Products.eXtremeManagement.utils import formatTime
from Products.statusmessages.interfaces import IStatusMessage
from webdav.Lockable import wl_isLocked, ResourceLockedError

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
      ...     def stories(self, sort_by_state=True, locked_status=False):
      ...         return []
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
       'locked': 0,
       'stories': [],
       'title': 'title',
       'uid': '1234'}

    We want to expand the list of story dicts with a 'class' item as that's
    too much calculating for the page template.

      >>> mock = [{'review_state': 'in-progress', 'uid': 'myuid', 'locked': False}]
      >>> new_mock = view.update_stories(mock)
      >>> new_mock[0]['class']
      'story-draggable state-in-progress kssattr-story_id-myuid'

    If the story is completed, it should not be draggable.

      >>> mock = [{'review_state': 'completed', 'uid': 'myuid', 'locked': False}]
      >>> new_mock = view.update_stories(mock)
      >>> new_mock[0]['class']
      'state-completed kssattr-story_id-myuid'

    It also should not be draggable if it's locked.

      >>> mock = [{'review_state': 'in-progress', 'uid': 'myuid', 'locked': True}]
      >>> new_mock = view.update_stories(mock)
      >>> new_mock[0]['class']
      'state-in-progress kssattr-story_id-myuid'

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
        stories = iteration_view.stories(sort_by_state=False, 
                                         locked_status=True)
        stories = self.update_stories(stories)
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
            locked = wl_isLocked(iteration),
        )
        return returnvalue

    def update_stories(self, stories):
        """Add a class to the stories' dicts"""
        format = '%(edit)sstate-%(review_state)s kssattr-story_id-%(uid)s'
        for story in stories:
            options = {'edit': 'story-draggable '}
            options.update(story)
            if story['review_state'] == 'completed' or story['locked']:
               # Don't make me draggable
               options['edit'] = ''
            story['class'] = format % options
             
        return stories


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
      ...     def getId(self):
      ...         return self.dict['id']
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

    The story is moved using standard zope cut/paste.

      >>> class MockDir(object):
      ...     objects = {}
      ...     def manage_cutObjects(self, ids):
      ...         to_return = {}
      ...         for id in ids:
      ...             to_return[id] = self.objects.pop(id)
      ...         return to_return
      ...     def manage_pasteObjects(self, cutdata):
      ...         self.objects.update(cutdata)
      ...     def objectIds(self):
      ...         return self.objects.keys()
      >>> source = MockDir()
      >>> target = MockDir()
      >>> source.objects = {'1': 1, '2': 2}
      >>> target.objects = {'3': 3}
      >>> story = MockBrainObject(id='1')
      >>> view.move(source, target, story)
      >>> source.objectIds()
      ['2']
      >>> target.objectIds()
      ['1', '3']

    """

    @kssaction
    def move_story(self, source_id, target_id, story_id, index):
        core = self.getCommandSet('core')
        plone = self.getCommandSet('plone')
        cns = self.getCommandSet('cns')
        source, target, story = self.extract_objects(source_id,
                                                     target_id,
                                                     story_id)
        if source == None: # The rest is also None.
            plone.issuePortalMessage(_(u'Drag/drop uids incorrect'),
                                     msgtype='error')
            return

        logger.info('%s dragged from %s to %s', story, source, target)
        if source != target:
            # Source and target are different: move the story.
            # Apparently it's possible for this story to be 'locked' - we'd 
            # better be ready for that...
            try:
                self.move(source, target, story)
            except ResourceLockedError:
                logger.info('Resource locked')
                IStatusMessage(self.request).addStatusMessage(
                    _(u"Move failed: story locked. "
                      u"Unlock the story to move it."), 
                    type='error')
                cns.redirectRequest(story.absolute_url())
                return

            msg = _(u'label_moved_succesfully',
                    default=u"Moved story '${story}' to iteration '${target}'.",
                    mapping={'story': story.Title(),
                             'target': target.Title()})
            plone.issuePortalMessage(msg, msgtype='info')
            # We have to set the right kssattr again now that our parent has
            # changed.
            format = 'kssattr-source_id-%s'
            old = format % source_id
            new = format % target_id
            node = core.getHtmlIdSelector(story_id)
            core.removeClass(node, old)
            core.addClass(node, new)

        # Give the dragged object the right position.
        target.moveObjectToPosition(story.getId(), int(index))
        putils = getToolByName(self.context, 'plone_utils')
        putils.reindexOnReorder(target)
        logger.info('Story %s now has position %s in the target folder.',
                    story, index)

        if source == target:
            # We haven't moved the object to another iteration, so that didn't
            # give us a status message. To provide feedback that something
            # happened we'll say that the object's position has been modified.
            msg = _(u'label_order_updated_succesfully',
                    default=(u"The position of story '${story}' in the "
                             u"iteration has been changed."),
                    mapping={'story': story.Title()})
            plone.issuePortalMessage(msg, msgtype='info')
            
    def extract_objects(self, source_id, target_id, story_id):
        """Return tuple of source/target/story objects"""
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

    def move(self, source, target, story):
        """Actually cut/paste the story from source to target iteration"""
        cutdata = source.manage_cutObjects(ids=[story.getId()])
        target.manage_pasteObjects(cutdata)
