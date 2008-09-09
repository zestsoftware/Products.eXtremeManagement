#from zope.cachedescriptors.property import Lazy
from zope.component import getMultiAdapter

from Products.eXtremeManagement.browser.projects import ProjectView
#from Products.eXtremeManagement.utils import formatTime
from Products.eXtremeManagement.browser.interfaces import IIterationView


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
      >>> zope.component.provideAdapter(factory=MockIterationView,
      ...                               adapts=(None, None),
      ...                               provides=IIterationView,
      ...                               name=u'iteration')


      >>> brain = MockBrain(Title='title', Description='desc',
      ...                   getObject=lambda: None)
      >>> from pprint import pprint
      >>> result = view.iterationbrain2dict(brain)
      >>> pprint(result)
      {'brain': <Products.eXtremeManagement.browser.reorderstories.MockBrain ...>,
       'description': 'desc',
       'stories': 'list of stories',
       'title': 'title'}

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
        )
        return returnvalue
