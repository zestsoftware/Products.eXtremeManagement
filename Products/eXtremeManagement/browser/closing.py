from Products.Five.browser import BrowserView
from zope.cachedescriptors.property import Lazy
from zope import component
from zope import interface


class IterationClosingView(BrowserView):
    """Browser view for closing an iteration and migrating unfinished
    stories to a target iteration.

      >>> class Mock(object):
      ...     def __init__(self, **kwargs):
      ...         self.__dict__.update(kwargs)
      >>> class MockFolder(object):
      ...     def __init__(self, contents=[], uid=None):
      ...         self.uid = uid
      ...         self.contents = contents
      ...     def UID(self):
      ...         return self.uid
      ...     def getFolderContents(self, *args, **kwargs):
      ...         return self.contents

      >>> from zope.component import provideAdapter
      >>> from zope.interface import Interface
      >>> project = MockFolder(
      ...     [Mock(Title='Iteration1',
      ...           getURL=lambda: 'http://somehost.com/iteration1',
      ...           UID='Iteration1'),
      ...      Mock(Title='Iteration2',
      ...           getURL=lambda: 'http://somehost.com/iteration2',
      ...           UID='Iteration2')])
      >>> class MockState(object):
      ...     def __init__(self, context, request):
      ...         self.project = project
      >>> provideAdapter(MockState, (MockFolder, Mock), Interface,
      ...                u'xm_global_state')

      >>> context = MockFolder(
      ...     [Mock(Title='Story1',
      ...           getURL=lambda: 'http://somehost.com/story1'),
      ...      Mock(Title='Story2',
      ...           getURL=lambda: 'http://somehost.com/story2')],
      ...     'Iteration1')

      >>> view = IterationClosingView(context, Mock())
      >>> [x['title'] for x in view.pending_stories]
      ['Story1', 'Story2']

      >>> [x['title'] for x in view.target_iterations]
      ['Iteration2']

    """

    story_crit = dict(portal_type='Story',
                      review_state=('in-progress', 'new'))
    target_iteration_crit = dict(portal_type='Iteration',
                                 review_state=('in-progress', 'new'))

    @Lazy
    def pending_stories(self):
        stories = self.context.getFolderContents(self.story_crit)
        return [{'title': x.Title,
                 'url': x.getURL()}
                for x in stories]

    @Lazy
    def target_iterations(self):
        state = component.getMultiAdapter(
            (self.context, self.request),
            interface.Interface,
            u'xm_global_state')
        project = state.project
        thisUID = self.context.UID()
        iterations = project.getFolderContents(self.target_iteration_crit)
        return [{'title': x.Title,
                 'url': x.getURL(),
                 'uid': x.UID}
                for x in iterations if x.UID != thisUID]

    def handle_close(self):
        return ''

    def __call__(self):
        submit = self.request.form.get('submit', None)
        if submit == 'Cancel':
            self.request.response.redirect(self.context.absolute_url()+'/view')
            return ''
        elif submit == 'Close Iteration':
            return self.handle_close()

        return self.index()
