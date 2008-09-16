from Products.Five.browser import BrowserView
from zope.cachedescriptors.property import Lazy
from zope import component
from datetime import date
from xm.charting import gantt
from xm.charting import model as chmodel


def pydate(dt):
    if dt is not None:
        return date(dt.year(), dt.month(), dt.day())
    return None


class GanttView(BrowserView):
    """A view for displaying a gantt chart.

      >>> class Mock(object):
      ...     def __init__(self, **kw): self.__dict__.update(kw)
      >>> gantt = GanttView(None, None)

    Getting the work hours is mostly about checking task estimates against
    assignees.

      >>> def search(**kw):
      ...     return [Mock(estimate=0, getAssignees=[]),
      ...             Mock(estimate=4, getAssignees=['someperson'])]
      >>> gantt._search = search
      >>> gantt._get_work_hours(Mock(getPath=lambda: 'foo'))
      {'someperson': 4.0}

    Durations are analogous to iterations.

      >>> from DateTime import DateTime
      >>> def search(**kw):
      ...     return [Mock(getObject=lambda: Mock(getStartDate=DateTime, getEndDate=DateTime),
      ...                  Title='Foo',
      ...                  getPath=lambda: 'somepath',
      ...                  estimate=1.0,
      ...                  review_state='private',
      ...                  getURL=lambda: 'http://somewhere',
      ...                  getAssignees=[])]
      >>> gantt._search = search
      >>> gantt._get_durations(Mock(getPath=lambda: 'foo'))
      [<xm.charting.model.Duration object ...>]

    """


    project_crit = dict(portal_type='Project',
                        sort_on='sortable_title',
                        review_state=('active', 'private'))
    iteration_crit = dict(portal_type='Iteration',
                          review_state=('in-progress', 'new'),
                          sort_on='getObjPositionInParent')
    task_crit = dict(portal_type='Task')

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @Lazy
    def _search(self):
        portal_state = component.getMultiAdapter((self.context, self.request),
                                                 name=u'plone_portal_state')
        portal = portal_state.portal()
        return portal.portal_catalog

    def _get_work_hours(self, itbrain):
        hours = {}
        for taskbrain in self._search(path=itbrain.getPath(),
                                      **self.task_crit):
            estimate = getattr(taskbrain, 'estimate', 0.0)
            if not estimate or estimate <= 0 or \
                   len(taskbrain.getAssignees) == 0:
                continue

            h = float(taskbrain.estimate) / float(len(taskbrain.getAssignees))
            for x in taskbrain.getAssignees:
                cur = hours.get(x, 0.0) + h
                hours[x] = cur
        return hours

    def _get_durations(self, prjbrain):
        durations = []
        for itbrain in self._search(path=prjbrain.getPath(),
                                    **self.iteration_crit):

            # getting object here due to end/start not being in indexes
            it = itbrain.getObject()
            d = chmodel.Duration(itbrain.Title,
                                 pydate(it.getStartDate()),
                                 pydate(it.getEndDate()),
                                 itbrain.review_state,
                                 itbrain.getURL())

            # finish getting the work hours bottom half of the chart
            # working
            d.work_hours = self._get_work_hours(itbrain)
            durations.append(d)

        return durations

    def _get_projects(self):
        projects = []
        # TODO: investigate *just* using indexes
        for prjbrain in self._search(**self.project_crit):
            durations = self._get_durations(prjbrain)
            if len(durations) == 0:
                continue

            dg = chmodel.DurationGroup(prjbrain.Title, prjbrain.getURL())
            dg._iterations += durations
            projects.append(dg)

        return projects

    def __call__(self):
        return gantt.generate_chart(self._get_projects())
