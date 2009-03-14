import logging
from zope import component
from zope import interface
from zope.cachedescriptors.property import Lazy
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore import utils as cmfutils

logger = logging.getLogger('xm')


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
    non_complete_stories = ('draft', 'pending', 'estimated', 'in-progress')
    non_complete_tasks = ('to-do', 'open')
    story_crit = dict(portal_type='Story',
                      review_state=non_complete_stories)
    target_iteration_crit = dict(portal_type='Iteration',
                                 review_state='new')

    iteration_close_state = ViewPageTemplateFile('iteration-close-state.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request
        state = component.getMultiAdapter((self.context, self.request),
                                          interface.Interface,
                                          u'xm_global_state')
        self.project = state.project

        pview = component.getMultiAdapter((self.context, self.request),
                                          interface.Interface,
                                          u'plone_portal_state')

        self.portal = portal = pview.portal()
        self.catalog = portal.portal_catalog

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

    def migrate_stories(self, targetit):
        pendingids = [x.getId
                      for x in self.context.getFolderContents(self.story_crit)]
        copy = self.context.manage_copyObjects(ids=pendingids)
        targetit.manage_pasteObjects(copy)
        for x in self.context.getFolderContents(self.story_crit):
            # delete all tasks that were completed from the target story
            xobj = x.getObject()
            for y in xobj.getFolderContents({'portal_type': 'Task',
                                             'review_state': 'completed'}):
                    targetit[x.getId].manage_delObjects([y.getId])

            self.remove_bookings(xobj)
            wf_tool = cmfutils.getToolByName(self.portal, 'portal_workflow')
            from Products.CMFCore.WorkflowCore import WorkflowException
            try:
                wf_tool.doActionFor(self.context, 'complete')
            except WorkflowException:
                pass
            

    def remove_bookings(self, obj):
        path = '/'.join(obj.getPhysicalPath())
        all = {}
        for x in self.catalog(portal_type='Booking', path='/'.join(path)):
            parent = x.getPath()[:-1]
            ids = all.get(parent, None)
            if ids is None:
                ids = all[parent] = set()
            ids.add(x.getId)

        for parentpath, ids in all.items():
            logger.info('Deleting from %r: %r' % (parentpath, ids))
            parent = self.portal.restrictedTraverse(parentpath)
            parent.manage_delObjects(ids)

        logger.info('Bookings cleaned up')

    def ensure_targetit(self):
        form = self.request.form
        uid = form.get('targetit', 'new')
        if uid == 'new':
            newtitle = form['title']
            newid = self.project.generateUniqueId(type_name='Iteration')
            self.project.invokeFactory(id=newid, type_name='Iteration')
            iteration = self.project[newid]
            iteration.update(title=newtitle)
            iteration._renameAfterCreation(check_auto_id=True)
            iteration.unmarkCreationFlag()
            iteration = self.project[iteration.getId()]
            logger.info('Created new iteration: %s' %
                        '/'.join(iteration.getPhysicalPath()))
        else:
            refcat = cmfutils.getToolByName(self.context, 'reference_catalog')
            iteration = refcat.lookupObject(uid)

        return iteration

    def handle_close(self):
        targetit = self.ensure_targetit()
        self.targetit = {'title': targetit.Title(),
                         'url': targetit.absolute_url()}
        self.migrate_stories(targetit)

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
