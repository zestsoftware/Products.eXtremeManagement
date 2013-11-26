Changelog
=========


2.1a4 (2013-11-26)
------------------

- Fix longstanding bug in reloading of task-form provider.  When doing
  a transition on a story, we now refresh the 'add task' part.
  [maurits]


2.1a3 (2012-09-12)
------------------

- Added zope.app.content as dependency.  Helps for Plone 4.2
  compatibility.  But Plone 4 is not officially supported yet.
  [maurits]

- Moved to github:
  https://github.com/zestsoftware/Products.eXtremeManagement
  [maurits]


2.1a2 (2011-02-03)
------------------

- Added upgrade step to recatalog the Stories, as their size_estimate
  in the catalog was broken when using xm.booking 2.0.
  [maurits]

- Get KSS portal status messages translated correctly again in Plone
  3.  Not used in Plone 4; not sure yet if this is needed there.
  [maurits]

- In the employees_overview also list members that are Employee
  because they are in a group that has the Employee role.  Patch by
  Yuri and Mauro.
  [maurits]

- In the employees_overview make the Employee name a link to see the
  task_overview for that Employee.  Patch by Yuri and Mauro.
  [maurits]


2.1a1 (2010-09-24)
------------------

- Added Plone 4 compatibility, while keeping Plone 3 compatibility.
  May have a few rough edges and has two failing tests on Plone 4
  (including one in xm.tracker), so use with care.
  [maurits]

- Avoid TraversalError in the xm.tracker when taskbrain2dict throws an
  AttributeError for a brain that fails getting its object.
  [maurits]

For older changes, see docs/HISTORY.txt.
