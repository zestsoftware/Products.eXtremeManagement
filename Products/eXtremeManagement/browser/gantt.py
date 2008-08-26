from Products.Five.browser import BrowserView
from zope import component
from datetime import date
from xm.charting import gantt
from xm.charting import model as chmodel


def pydate(dt):
    if dt is not None:
        return date(dt.year(), dt.month(), dt.day())
    return None


class GanttView(BrowserView):

    project_crit = dict(portal_type='Project',
                        sort_on='getObjPositionInParent')
    iteration_crit = dict(portal_type='Iteration',
                          review_state=('in-progress', 'new'),
                          sort_on='getObjPositionInParent')

    def __call__(self):
        portal_state = component.getMultiAdapter((self.context, self.request),
                                                 name=u'plone_portal_state')
        portal = portal_state.portal()
        search = portal.portal_catalog

        projects = []
        for prjbrain in search(**self.project_crit):
            dg = chmodel.DurationGroup(prjbrain.Title)
            projects.append(dg)
            for itbrain in search(path=prjbrain.getPath(),
                                  **self.iteration_crit):

                # TODO: investigate using indexes
                # getting object here due to end/start not being in indexes
                it = itbrain.getObject()
                dg._iterations.append(
                    chmodel.Duration(itbrain.Title,
                                     pydate(it.getStartDate()),
                                     pydate(it.getEndDate())),
                    )

        return gantt.generate_chart(projects)
