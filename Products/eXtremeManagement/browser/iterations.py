from StringIO import StringIO

from Acquisition import aq_inner, ImplicitAcquisitionWrapper
from Products.PageTemplates.PageTemplate import PageTemplate
from Products.CMFCore.utils import getToolByName

from Products.eXtremeManagement.browser.xmbase import XMBaseView

def _store_on_context(obj, *args, **kwargs):
    KEY = '_v_XM_cache'
    if not hasattr(obj.context.aq_base, KEY):
        setattr(obj.context, KEY, {})
    return getattr(obj.context, KEY)

def _render_details_cachekey(obj, storybrain):
    key = StringIO()
    catalog = getToolByName(obj.context, 'portal_catalog')
    for brain in catalog(portal_type='Task', path=storybrain.getPath()):
        key.write(brain.getPath())
        key.write('\n')
        key.write(brain.modified)
        key.write('\n\n')
    key.write(storybrain.getPath())
    return key.getvalue()

def cache(get_key, get_cache):
    def decorator(fun):
        def replacement(*args, **kwargs):
            key = get_key(*args, **kwargs)
            cache = get_cache(*args, **kwargs)
            cached_value = cache.get(key)
            if cached_value is None:
                cache[key] = fun(*args, **kwargs)
            return cache[key]
        return replacement
    return decorator

def degrade_headers(html, howmuch=2):
    """
      >>> degrade_headers('<h1>Hello</h1><h2>World</h2>')
      '<h3>Hello</h3><h4>World</h4>'
      >>> degrade_headers('<h0>Funny things</h0><h2>as input</h2>')
      '<h2>Funny things</h2><h4>as input</h4>'
    """
    for number in range(6, -1, -1):
        html = html.replace('<h%s' % number, '<h%s' % (number + howmuch))
        html = html.replace('</h%s>' % number, '</h%s>' % (number + howmuch))
    return html

class IterationView(XMBaseView):
    """Simply return info about a Iteration.
    """

    details_template = PageTemplate()
    details_template.write("""
    <metal:define metal:use-macro='context/global_defines/macros/defines' />
    <h0 tal:content='context/Title'>Story title</h0>
    <metal:use use-macro='context/story_view/macros/details' />
    """)
    

    def main(self):
        """Get a dict with info from this Context.
        """
        context = aq_inner(self.context)
        workflow = getToolByName(context, 'portal_workflow')
        returnvalue = dict(
            title = context.Title(),
            description = context.Description(),
            man_hours = context.getManHours(),
            start_date = context.restrictedTraverse('@@plone').toLocalizedTime(context.getStartDate()),
            end_date = context.restrictedTraverse('@@plone').toLocalizedTime(context.getEndDate()),
            estimate = self.xt.formatTime(context.getRawEstimate()),
            actual = self.xt.formatTime(context.getRawActualHours()),
            difference = self.xt.formatTime(context.getRawDifference()),
            review_state = workflow.getInfoFor(context, 'review_state'),
            )
        return returnvalue

    def stories(self):
        context = aq_inner(self.context)
        filter = dict(portal_type='Story',
                      sort_on='getObjPositionInParent')
        items = context.getFolderContents(filter)
        storybrains = self.xt.getStateSortedContents(items)

        story_list = []

        for storybrain in storybrains:
            info = self.storybrain2dict(storybrain)
            info['details'] = self.render_details(storybrain)
            story_list.append(info)

        return story_list

    def storybrain2dict(self, brain):
        """Get a dict with info from this story brain.
        """
        context = aq_inner(self.context)
        review_state_id = brain.review_state
        workflow = getToolByName(context, 'portal_workflow')
        catalog = getToolByName(context, 'portal_catalog')

        # compute progress percentage
        is_completed = (review_state_id == 'completed')
        if is_completed:
            progress = 100
        else:
            estimated = brain.getRawEstimate
            actual = brain.getRawActualHours
            progress = self.xt.get_progress_perc(actual, estimated)

        # compute open task count
        searchpath = brain.getPath()
        filter = dict(portal_type=['Task', 'PoiTask'],
                      path=searchpath)
        unfinished_states = ('open','to-do',)
        filter['review_state'] = unfinished_states
        open_tasks = len(catalog.searchResults(**filter))

        # compute completed task count
        finished_states = ('completed',)
        filter['review_state'] = finished_states
        completed_tasks = len(catalog.searchResults(**filter))

        returnvalue = dict(
            url = brain.getURL(),
            title = brain.Title,
            description = brain.Description,
            estimate = self.xt.formatTime(brain.getRawEstimate),
            actual = self.xt.formatTime(brain.getRawActualHours),
            difference = self.xt.formatTime(brain.getRawDifference),
            progress = progress,
            review_state = review_state_id,
            review_state_title = workflow.getTitleForStateOnType(
                                 review_state_id, 'Story'),
            is_completed = is_completed,
            open_tasks = open_tasks,
            completed_tasks = completed_tasks,
        )
        return returnvalue

    def todo_tasks(self):
        return self.state_tasks('to-do')

    def open_tasks(self):
        return self.state_tasks('open')

    def state_tasks(self, state):
        context = aq_inner(self.context)
        context.REQUEST.form['state'] = state
        view = context.restrictedTraverse('@@mytask_details')
        result = view.tasklist()
        return result

    @cache(_render_details_cachekey, _store_on_context)
    def render_details(self, storybrain):
        story = storybrain.getObject()
        info = story.restrictedTraverse('@@story').main()
        rendered = ImplicitAcquisitionWrapper(self.details_template, story)()
        return degrade_headers(rendered)
