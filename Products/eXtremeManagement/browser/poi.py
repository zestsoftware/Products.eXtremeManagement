from zope import interface
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.interfaces import IReferenceable
from Products.statusmessages.interfaces import IStatusMessage

class IPoiView(interface.Interface):
    """See doc/poi-integration.txt"""
    
    def add_tasks_from_tags(tags):
        """Takes a number of tags and looks for issues in the project
        that have those tags.  Adds those issues to the current
        folder as Poi Tasks if they don't already exist.
        """

    def can_add_tasks():
        """Return true if context is a story to which we can add tasks
        and there are tags/issues available for selection.
        """

    def available_tags():
        """Returns a list of tags as strings that can be chosen for
        adding tasks from them in the current context (=story)."""

    def links():
        """A list of dicts containing information about tasks that the
        current context (=issue) is linked from.
        """


class PoiView(BrowserView):
    def get_open_issues(self, tags=[]):
        query = {}
        if tags:
            query = dict(Subject=dict(query=tags, operator='and'))
        issues = self.get_open_issues_in_project(**query)
        # Hopefully, there aren't too many open issues :)
        issues = [b.getObject() for b in issues]
        
        # Skip issues that are already linked into this iteration:
        iteration = self.context.aq_inner.aq_parent
        iteration_path = '/'.join(iteration.getPhysicalPath())
        def is_linked_into_iteration(issue):
            tasks = issue.getBRefs('task_issues')
            for task in tasks:
                path = '/'.join(task.getPhysicalPath())
                if path.startswith(iteration_path):
                    return True
            else:
                return False
        ignore = [i for i in issues if is_linked_into_iteration(i)]
        return ([i for i in issues if i not in ignore], ignore)
    
    def get_open_issues_in_project(self, **kwargs):
        project = self._lookup_project()
        assert project.portal_type == 'Project', "Failed to associated project."
        catalog = getToolByName(self.context, 'portal_catalog')
        query = dict(portal_type='PoiIssue',
                     review_state=['in-progress', 'open',
                                   'unconfirmed', 'new'],
                     path='/'.join(project.getPhysicalPath()))
        query.update(kwargs)
        return catalog(**query)

    def _lookup_project(self):
        item = self.context.aq_inner
        while item is not None and item.portal_type != 'Project':
            item = getattr(item, 'aq_parent', None)
        return item

    def add_tasks_from_tags(self, tags):
        issues, ignore = self.get_open_issues(tags)
        for issue in issues:
            name = 'issue-%s' % issue.getId()
            self.context.invokeFactory('PoiTask',
                                       id=name,
                                       title=issue.Title(),
                                       issues=[issue])

        addMessage = IStatusMessage(self.request).addStatusMessage
        if len(issues):
            names = ', '.join([i.Title() or i.getId() for i in issues])
            addMessage('Added tasks for issues: %s.' % names, type='info')
        else:
            msg = 'Found no issues matching tags: %s.' % ', '.join(tags)
            if len(ignore):
                names = ', '.join([i.Title() or i.getId() for i in ignore])
                msg += (' These issues already have corresponding tasks in '
                        'this iteration: %s.' % names)
            addMessage(msg, type='info')

    def can_add_tasks(self):
        if 'PoiTask' not in [fti.getId() for fti in
                             self.context.allowedContentTypes()]:
            return False
        elif self.available_tags():
            return True
        else:
            return False

    def available_tags(self):
        tags = dict()
        for issue in self.get_open_issues()[0]:
            for s in issue.Subject():
                tags[s] = 1
        keys = tags.keys()
        keys.sort(lambda x, y: cmp(x.lower(), y.lower()))
        return keys

    def links(self):
        if not IReferenceable.providedBy(self.context):
            return []
        
        value = []
        workflow = getToolByName(self.context, 'portal_workflow')

        tasks = self.context.getBRefs('task_issues')
        tasks = sorted(tasks,
                       lambda a,b: cmp(a.ModificationDate(),
                                       b.ModificationDate()))
        for task in tasks:
            value.append(
                dict(title=task.Title() or task.getId(),
                     url=task.absolute_url(),
                     state=workflow.getInfoFor(task, 'review_state'))
                )
        return value

    def __call__(self):
        tags = self.request.get('tags', [])
        if tags:
            self.add_tasks_from_tags(tags)
        self.request.RESPONSE.redirect(self.context.absolute_url())
        return ''
