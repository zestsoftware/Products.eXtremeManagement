import Acquisition
import Products.Five
import zope.interface
from Products.eXtremeManagement import interfaces
from Products.CMFCore import utils as cmfutils

def find_provides(context, iface, limit=10):
    """Travel up the acquisition chain to find the closest object that
    provides the 'iface' interface.  The 'limit' arg ensures if there
    is any possible infinite recursion it will stop at limit.

    """

    obj = context
    for x in range(limit):
        if iface.providedBy(obj):
            return obj
        obj = Acquisition.aq_parent(Acquisition.aq_inner(obj))
        if obj is None:
            return None
    return None

ACTIONS = {'copy': u'copy as new',
           'use_existing': u'use existing (%(target)s)',
           'close_use_existing': u'close existing (%(source)s) and use '
                                 u'existing target (%(target)s)',
           'close_copy': u'close existing (%(source)s) and copy as new',
           'none_no_carry_over': u'cannot be carried over'}

def serialize_action_state(story_actions):
    """Take the given story actions and seralize to a state that can
    be converted to a string for easy transporation.

    """

    state = []
    for story_action in story_actions:
        key = 'stories:list'
        value = story_action['source_uid']
        state.append({'key': key, 'value': value})

        key = 'source_story_'+story_action['source_uid']
        value = story_action['action']
        state.append({'key': key, 'value': value})

        if story_action['target_uid']:
            key = 'target_story_'+story_action['source_uid']
            value = story_action['target_uid']
            state.append({'key': key, 'value': value})

        for task_action in story_action['task_actions']:
            key = 'source_story_tasks_'+story_action['source_uid']+':list'
            value = task_action['source_uid']
            state.append({'key': key, 'value': value})

            key = 'source_task_'+task_action['source_uid']
            value = task_action['action']
            state.append({'key': key, 'value': value})

            if task_action['target_uid']:
                key = 'target_task_'+task_action['source_uid']
                value = task_action['target_uid']
                state.append({'key': key, 'value': value})

    return state

def extract_story_actions(request):
    """Build a list of dicts which represent the actions that need to be
    performed for stories and tasks from a request-style dict.

    """

    stories = []
    for story_uid in request.get('stories', []):
        task_uids = request.get('source_story_tasks_'+story_uid, [])
        tasks = []
        for task_uid in task_uids:
            task_action = {'source_uid': task_uid,
                           'action': request.get('source_task_'+task_uid, ''),
                           'target_uid': request.get('target_task_'+task_uid,
                                                     '')}
            tasks.append(task_action)

        story = {'source_uid': story_uid,
                 'target_uid': request.get('target_story_'+story_uid, ''),
                 'action': request.get('source_story_'+story_uid),
                 'task_actions': tasks}

        stories.append(story)

    return stories

class BadActionError(ValueError): pass

def perform_story_actions(target_iteration, actions):
    refcat = cmfutils.getToolByName(target_iteration, 'reference_catalog')
    wftool = cmfutils.getToolByName(target_iteration, 'portal_workflow')

    for story_action in actions:
        story = refcat.lookupObject(story_action['source_uid'])

        if story_action['action'].endswith('copy'):
            parent = Acquisition.aq_parent(story)
            data = parent.manage_copyObjects([story.getId()])
            target_iteration.manage_pasteObjects(data)
            target_story = target_iteration[story.getId()]

            # remove tasks
            target_story.manage_delObjects(target_story.objectIds())
        elif story_action['action'].endswith('use_existing'):
            target_story = refcat.lookupObject(story_action['target_uid'])
        else:
            raise BadActionError(story_action['action'])

        for task_action in story_action['task_actions']:
            task = refcat.lookupObject(task_action['source_uid'])

            if task_action['action'].endswith('copy'):
                parent = Acquisition.aq_parent(task)
                data = parent.manage_copyObjects([task.getId()])
                target_story.manage_pasteObjects(data)
                target_task = target_story[task.getId()]

                # remove bookings
                target_task.manage_delObjects(target_task.objectIds())

                target_task.setCarriedOverFrom(task)
                target_task.reindexObject()
            elif task_action['action'] != 'none_no_carry_over':
                raise BadActionError(task_action['action'])

            if task_action['action'].startswith('close'):
                wftool.doActionFor(task, 'carry-over')

        if story_action['action'].startswith('close'):
            wftool.doActionFor(story, 'carry-over')

        target_story.setCarriedOverFrom(story)
        target_story.reindexObject()

class ICarryOver(zope.interface.Interface):
    def possible_iterations(): pass
    def targetted_iteration(): pass
    def story_actions(): pass
    def safe_action_state(): pass
    def perform_actions(): pass

class CarryOver(Products.Five.BrowserView):
    zope.interface.implements(ICarryOver)

    def possible_iterations(self):
        project = find_provides(self.context,
                                interfaces.IXMProject)
        iteration = find_provides(self.context,
                                  interfaces.IXMIteration)
        cf = {'portal_type': 'Iteration',
              'review_state': ['new', 'in-progress']}
        contents = project.getFolderContents(contentFilter=cf)
        path = iteration and '/'.join(iteration.getPhysicalPath()) or None

        res = [{'title': x.Title, 'UID': x.UID}
               for x in contents if x.getPath() != path]

        return res

    def targetted_iteration(self):
        if hasattr(self, '_cached_target_iteration'):
            return self._cached_target_iteration[0]

        uid = self.request.get('iteration', None)
        if not uid:
            raise ValueError('Request has no appropriate iteration param')

        refcat = cmfutils.getToolByName(self.context, 'reference_catalog')
        target_it = refcat.lookupObject(uid)
        if target_it is None:
            raise LookupError(uid)
        self._cached_target_iteration = [target_it]

        return self._cached_target_iteration[0]

    def _existing(self, newparent, source):
        if newparent is None:
            return None

        if source['id'] in newparent.objectIds():
            obj = newparent[source['id']]
            if interfaces.IXMStory.providedBy(obj):
                return obj

        cf = {'Title': source['title']}
        contents = newparent.getFolderContents(contentFilter=cf)
        if len(contents) > 0:
            obj = contents[0].getObject()
            return obj

        return None

    def _update_story_for_target(self, story_action, should_close_story):
        refcat = cmfutils.getToolByName(self.context, 'reference_catalog')
        wftool = cmfutils.getToolByName(self.context, 'portal_workflow')
        target_it = self.targetted_iteration()
        source_story = refcat.lookupObject(story_action['source_uid'])
        target_story = None

        target_story = self._existing(target_it, story_action)
        if target_story is not None:
            story_action['action'] = 'use_existing'
            story_action['target_uid'] = target_story.UID()
        elif 'carry-over' in wftool.getActionsFor(source_story):
            story_action['action'] = 'copy'
        else:
            story_action['action'] = 'none_no_carry_over'

        for task in story_action['task_actions']:
            source_task = refcat.lookupObject(task['source_uid'])
            target_task = None

            if 'carry-over' not in wftool.getActionsFor(source_task):
                task['action'] = 'none_no_carry_over'
            else:
                target_task = self._existing(target_story, task)
                if target_task is not None:
                    task['action'] = 'use_existing'
                    task['target_uid'] = target_task.UID()
                else:
                    task['action'] = 'close_copy'

            target = target_task and target_task.title_or_id() or 'N/A'
            source = source_task.title_or_id()
            task['action_label'] = ACTIONS[task['action']] \
                                   % {'source': source, 'target': target}

        target = target_story and target_story.title_or_id() or 'N/A'
        source = source_story.title_or_id()

        story_action['action_label'] = ACTIONS[story_action['action']] \
                                       % {'source': source, 'target': target}

    def _task_action(self, task):
        task = Acquisition.aq_inner(task)
        return {'id': task.getId(),
                'title': task.Title(),
                'action_label': 'N/A',
                'source_uid': task.UID(),
                'target_uid': ''}

    def _story_action(self, story, task_actions):
        story = Acquisition.aq_inner(self.context)
        return {'id': story.getId(),
                'title': story.Title(),
                'task_actions': task_actions,
                'action_label': 'N/A',
                'source_uid': story.UID(),
                'target_uid': ''}

    def story_actions(self):
        stories = []
        if interfaces.IXMTask.providedBy(self.context):
            story = Acquisition.aq_parent(Acquisition.aq_inner(self.context))
            task_actions = [self._task_action(self.context)]
            story_action = self._story_action(story, task_actions)

            self._update_story_for_target(story_action, False)
            stories.append(story_action)
        elif interfaces.IXMStory.providedBy(self.context):
            task_actions = []
            story = Acquisition.aq_inner(self.context)
            for task in story.contentValues():
                task_actions.append(self._task_action(task))
            story_action = self._story_action(story, task_actions)
            self._update_story_for_target(story_action, True)
            stories.append(story_action)

        return stories

    def safe_action_state(self):
        return serialize_action_state(self.story_actions())

    def perform_actions(self):
        return perform_story_actions(self.targetted_iteration(),
                                     extract_story_actions(self.request))

    def __call__(self, *args, **kwargs):
        form = self.context.restrictedTraverse('xm-carry-over-form')
        return form(*args, **kwargs)
