import textwrap

from Acquisition import aq_inner, aq_parent
from zope import interface
from zope.component import queryMultiAdapter
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.interfaces import IReferenceable
from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFPlone.utils import safe_unicode

from Products.eXtremeManagement.interfaces.xmissuegetter import IXMIssueGetter
from Products.eXtremeManagement.browser.xmbase import XMBaseView


def abbreviate(text, width=15, ellipsis='...'):
    """Abbreviate a given text.

      >>> abbreviate('This is an unnecessarily long piece of text!')
      'This is an...'
      >>> abbreviate('Quite short, but still')
      'Quite short,...'
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


class PoiView(XMBaseView):
    request = None
    context = None

    def _get_open_issues(self, tags=[]):
        query = {}
        if tags:
            query = dict(Subject=dict(query=tags, operator='and'))
        issues_brains = self.get_open_issues_in_project(**query)
        # This method is now only called when *adding* issues.
        issues = [b.getObject() for b in issues_brains]

        # Skip issues that are already linked into this iteration:
        iteration = aq_parent(aq_inner(self.context))
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
        context = aq_inner(self.context)
        issue_getter = queryMultiAdapter((context, self.request),
                                         IXMIssueGetter)
        if issue_getter is None:
            # We're being called from something for which there's no adapter.
            return []
        return issue_getter.get_issues(**kwargs)

    def get_open_stories_in_project(self, **kwargs):
        return self.get_open_issues_in_project(
            portal_type='Story',
            review_state=['estimated', 'in-progress'])

    def _lookup_project(self):
        item = aq_inner(self.context)
        while (item is not None and
               getattr(item, 'portal_type', None) != 'Project'):
            item = aq_parent(item)
        return item

    def _add_message(self, message, type='info'):
        addMessage = IStatusMessage(self.request).addStatusMessage
        addMessage(safe_unicode(message), type)

    def add_tasks_from_tags(self, tags):
        issues, ignore = self._get_open_issues(tags)
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
            if story.portal_type != 'Story':
                return False

        types = getToolByName(self.context, 'portal_types')
        task_type = types.getTypeInfo('PoiTask')
        return task_type.isConstructionAllowed(story)

    def available_tags(self):
        tags = dict()
        # XXX
        for issue in self.get_open_issues_in_project():
            for s in issue.Subject:
                tags[s] = 1
        keys = tags.keys()
        keys.sort(lambda x, y: cmp(x.lower(), y.lower()))
        return keys

    def links(self):
        if not IReferenceable.providedBy(self.context):
            return []

        value = []

        tasks = self.context.getBRefs('task_issues')
        tasks = sorted(tasks,
                       lambda a, b: cmp(a.ModificationDate(),
                                       b.ModificationDate()))
        for task in tasks:
            value.append(
                dict(iterationid=task.getPhysicalPath()[-3],
                     title=abbreviate(task.Title() or task.getId(), width=25),
                     url=task.absolute_url(),
                     state=self.workflow.getInfoFor(task, 'review_state')))
        return value

    def stories_to_add_to(self):
        value = []
        for story in self.get_open_stories_in_project():
            story = story.getObject()
            if not self.can_add_tasks(story):
                continue
            value.append(
                dict(iterationid=story.getPhysicalPath()[-2],
                     uid=story.UID(),
                     title=abbreviate(story.Title() or story.getId(), width=80)))
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
        title = '#%s: %s' % (issue.getId(), issue.Title())
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
