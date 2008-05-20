from zope.interface import implements
from Products.Archetypes import atapi

from Products.eXtremeManagement.content.Task import Task
from Products.eXtremeManagement.interfaces.xmtask import IIssueTask


class PoiTask(Task):
    portal_type = meta_type = 'PoiTask'
    archetype_name = 'Issue Tracker Task'
    implements(IIssueTask)

    schema = Task.schema.copy() + atapi.Schema((
        atapi.ReferenceField('issues',
                             multiValued=1,
                             relationship='task_issues',
                             allowed_types=('PoiIssue', ),
                             vocabulary='vocabulary_issues',
                             ),
        ))

    schema.moveField('issues', after='title')
    schema['mainText'].widget.visible = dict(edit=0, view=0)
    schema['assignees'].widget.visible = dict(edit=0, view=1)

    def vocabulary_issues(self):
        pairs = []
        poiview = self.restrictedTraverse('@@xm-poi')
        for brain in poiview.get_open_issues_in_project():
            issue = brain.getObject()
            label = '#%s: %s' % (issue.getId(), issue.Title())
            pairs.append((issue.UID(), label))
        # Guard against losing our issues when they are closed and we
        # still want to edit this PoiTask.  See
        # http://plone.org/products/extreme-management-tool/issues/58/
        keys = [key for key, value in pairs]
        for issue in self.getIssues():
            if issue.UID() not in keys:
                label = '#%s: %s' % (issue.getId(), issue.Title())
                pairs.append((issue.UID(), label))
        pairs = sorted(pairs, lambda a, b: cmp(a[1], b[1]))
        return atapi.DisplayList(pairs)

    def getAssignees(self):
        managers = set()
        for issue in self.getRefs('task_issues'):
            managers.add(issue.getResponsibleManager())
        return sorted(list(managers))

    def view(self):
        """
        """
        return self.poitask_view()

atapi.registerType(PoiTask, 'eXtremeManagement')
