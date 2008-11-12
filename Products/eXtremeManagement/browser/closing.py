from Products.Five.browser import BrowserView
from zope.cachedescriptors.property import Lazy
from zope import component
from zope import interface


class IterationClosingView(BrowserView):

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

    def __call__(self):
        submit = self.request.form.get('submit', None)
        if submit == 'Cancel':
            self.request.response.redirect(self.context.absolute_url()+'/view')
            return ''

        return self.index()
