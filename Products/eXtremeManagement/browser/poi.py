import textwrap

from zope import interface
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.interfaces import IReferenceable
from Products.statusmessages.interfaces import IStatusMessage

def abbreviate(text, width=18, ellipsis='...'):
    """Abbreviate a given text.

      >>> abbreviate('This is an unnecessarily long piece of text!')
      'This is an...'
      >>> abbreviate('Quite short, but still')
      'Quite short, but...'
      >>> abbreviate('Quite short, but still', width=10)
      'Quite...'
    """
    lines = textwrap.wrap(text, width)
    if len(lines) > 1:
        return lines[0] + '...'
    else:
        return lines[0]

class IPoiView(interface.Interface):
    """See doc/poi-integration.txt"""
    
    def add_tasks_from_tags(tags):
        """Takes a number of tags and looks for issues in the project
        that have those tags.  Adds those issues to the current
        folder as Poi Tasks if they don't already exist.
        """

    def can_add_tasks(story=None):
        """Return true if context (or story argument) is a story to
        which we can add tasks and there are tags/issues available for
        selection.
        """

    def available_tags():
        """Returns a list of tags as strings that can be chosen for
        adding tasks from them in the current context (=story)."""

    def links():
        """A list of dicts containing information about tasks that the
        current context (=issue) is linked from.
        """
    def stories_to_add_to():
        """Returns a dict with information about stories that we can
        add tasks to.
        """


class PoiView(BrowserView):
    def get_open_issues(self, tags=[], skip_existing_issues=True):
        query = {}
        if tags:
            query = dict(Subject=dict(query=tags, operator='and'))
        issues = self.get_open_issues_in_project(**query)
        # Hopefully, there aren't too many open issues :)
        issues = [b.getObject() for b in issues]

        if skip_existing_issues:
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
        else:
            is_linked_into_iteration = lambda issue: False
        
        ignore = [i for i in issues if is_linked_into_iteration(i)]
        return ([i for i in issues if i not in ignore], ignore)
    
    def get_open_issues_in_project(self, **kwargs):
        project = self._lookup_project()
        assert project.portal_type == 'Project', (
            "Failed to get associated project.")
        catalog = getToolByName(self.context, 'portal_catalog')
        query = dict(portal_type='PoiIssue',
                     review_state=['in-progress', 'open',
                                   'unconfirmed', 'new'],
                     path='/'.join(project.getPhysicalPath()))
        query.update(kwargs)
        return catalog(**query)

    def get_open_stories_in_project(self, **kwargs):
        return self.get_open_issues_in_project(
            portal_type='Story',
            review_state=['estimated', 'draft', 'pending'])
            
        project = self._lookup_project()
        assert project.portal_type == 'Project', (
            "Failed to get associated project.")
        catalog = getToolByName(self.context, 'portal_catalog')

    def _lookup_project(self):
        item = self.context.aq_inner
        while item is not None and item.portal_type != 'Project':
            item = getattr(item, 'aq_parent', None)
        return item

    def _add_message(self, message, type='info'):
        addMessage = IStatusMessage(self.request).addStatusMessage
        addMessage(message, type)

    def add_tasks_from_tags(self, tags):
        issues, ignore = self.get_open_issues(tags)
        for issue in issues:
            self.add_issue_to_story(self.context, issue)
        
        if len(issues):
            names = ', '.join([i.Title() or i.getId() for i in issues])
            self._add_message('Added tasks for issues: %s.' % names)
        else:
            msg = 'Found no issues matching tags: %s.' % ', '.join(tags)
            if len(ignore):
                names = ', '.join([i.Title() or i.getId() for i in ignore])
                msg += (' These issues already have corresponding tasks in '
                        'this iteration: %s.' % names)
            self._add_message(msg)

    def can_add_tasks(self, story=None):
        if story is None:
            story = self.context
        
        if 'PoiTask' not in [fti.getId() for fti in
                             story.allowedContentTypes()]:
            return False
        elif self.available_tags():
            return True
        else:
            return False

    def available_tags(self):
        tags = dict()
        for issue in self.get_open_issues(skip_existing_issues=False)[0]:
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
                dict(iterationid=task.getPhysicalPath()[-3],
                     title=abbreviate(task.Title() or task.getId(), width=25),
                     url=task.absolute_url(),
                     state=workflow.getInfoFor(task, 'review_state'))
                )
        return value

    def stories_to_add_to(self):
        value = []
        for story in self.get_open_stories_in_project():
            # Ironically, to get something as light-weight as the UID,
            # we have to resort to getting the actual object:
            story = story.getObject()
            if not self.can_add_tasks(story):
                continue
            value.append(
                dict(iterationid=story.getPhysicalPath()[-2],
                     uid=story.UID(),
                     title=abbreviate(story.Title() or story.getId()))
                )
        return value

    def add_issue_to_story(self, story_or_uid, issue=None):
        if isinstance(story_or_uid, str):
            # It's a UID, convert
            references = getToolByName(self.context, 'reference_catalog')
            story = references.lookupObject(story_or_uid)
        else:
            story = story_or_uid

        if issue is None:
            issue = self.context

        name = 'issue-%s' % issue.getId()
        title = issue.Title()
        title = title and ('Task for %s' % title) or name
        while name in story.objectIds():
            name = 'copy-of-%s' % name
        if name.startswith('copy-of'):
            title = (title and 'Copy of %s' % title) or name
        
        story.invokeFactory('PoiTask',
                            id=name,
                            title=title,
                            issues=[issue])

    def __call__(self):
        tags = self.request.get('tags', [])
        story_uid = self.request.get('story')

        if tags:
            self.add_tasks_from_tags(tags)

        elif story_uid is not None:
            assert self.context.portal_type == 'PoiIssue', (
                "Trying to add non-issue %r." % self.context)
            self.add_issue_to_story(story_uid)
            self._add_message('Created new task.')

        self.request.RESPONSE.redirect(self.context.absolute_url())
        return ''
