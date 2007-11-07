"""Remove schema attribute from objects.

Some versions of Archetypes would add a schema attribute to your
content types when doing a schema update.  This is wrong.  It means
that subsequent schema updates would not actually work.  For me
(Maurits) it resulted in a 'KeyError: presentation' when viewing the
front-page on Plone 3.0.  This was fixed in Archetypes 1.5.2.

If you are bitten by this, add this as an ExternalMethod to your site
and run this.  It worked for me, but you do this at your own risk of
course so please make a backup before doing this.

"""

from Products.CMFCore.utils import getToolByName
from cStringIO import StringIO


def remove_schema_attributes(self):
    out = StringIO()
    catalog = getToolByName(self, 'portal_catalog')
    brains = catalog()
    print >> out, len(brains),  'brains found'
    count = 0
    for brain in brains:
        try:
            obj = brain.getObject()
        except AttributeError:
            print >> out, 'Ignoring dead brain pointing to', brain.getPath()
        if 'schema' in obj.__dict__:
            print >> out, 'Removing schema attribute from', obj.absolute_url()
            del obj.schema
            count += 1

    print >> out, ""
    print >> out, '--- In total', count, 'schemas were removed.'
    return out.getvalue()
