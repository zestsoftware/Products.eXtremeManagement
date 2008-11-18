from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore import utils as cmfutils
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

    iteration_close_state = ViewPageTemplateFile('iteration-close-state.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request
        state = component.getMultiAdapter(
            (self.context, self.request),
            interface.Interface,
            u'xm_global_state')
        self.project = state.project



    @Lazy
    def pending_stories(self):
        stories = self.context.getFolderContents(self.story_crit)
        return [{'title': x.Title,
                 'url': x.getURL()}
                for x in stories]

    @Lazy
    def target_iterations(self):
        thisUID = self.context.UID()
        iterations = self.project.getFolderContents(self.target_iteration_crit)
        return [{'title': x.Title,
                 'url': x.getURL(),
                 'uid': x.UID}
                for x in iterations if x.UID != thisUID]

    def close_iteration(self, sourceit, targetit):
        pass

    def ensure_targetit(self):
        form = self.request.form
        type_ = form.get('target_iteration_type', 'new')
        if type_ == 'new':
            newtitle = form['title']
            self.project.invokeFactory(title=newtitle)
            iteration = None
        else:
            uid = form['targetit']
            refcat = cmfutils.getToolByName(self.context, 'reference_catalog')
            iteration = refcat.lookupObject(uid)

        return iteration

    def handle_close(self):
        targetit = self.ensure_targetit()
        sourceit = self.context
        self.close_iteration(sourceit, targetit)
        return self.iteration_close_state()

    def __call__(self):
        submit = self.request.form.get('submit', None)
        form = self.request.form
        if form.get('cancel', None):
            self.request.response.redirect(self.context.absolute_url()+'/view')
            return ''
        elif form.get('close', None):
            return self.handle_close()

        return self.index()
