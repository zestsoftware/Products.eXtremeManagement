Installation
============

  Make a backup of your site.  You can never be too careful.

  We strongly advise using buildout; it is certainly not impossibly to
  get it to work in other ways but this is not supported.  Just add
  Products.eXtremeManagement in the main eggs section of your
  buildout.cfg.

  *Important*: you need to install egenix-mx-base from Egenix_.
  Either use the installers provided by them or use your own system
  tools (``apt-get install python-egenix-mxdatetime`` works on
  Debian/Ubuntu) or use ``easy_install egenix-mx-base``.  On Windows
  the installers seem to be the easiest way.
  For mac users, do:  sudo easy_install-2.4 egenix-mx-base
  Then open python terminal: python2.4
  >>import mx.DateTime

  Then restart your zope instance and use the Add/Remove products page
  in Site Setup to install eXtremeManagement.

.. _Egenix: http://egenix.com/


Dependencies
============

For reference, here are the dependencies:

  * Plone: 3.1 or 3.2 with Zope 2.10.

  * Some xm.* and kss.* packages and pygooglechart (pulled in
    automatically via setup.py)

  * Poi with its dependencies.  Get a bundle with products fit for the
    Plone version you are using: http://plone.org/products/poi

    With Poi installed, eXtremeManagement allows you to add an issue
    tracker in a project.  And you can add PoiTasks to Stories, which
    lets you easily link to existing issues in the tracker of your
    project.

  * The mx.DateTime library from Egenix_; see the Installation_
    instructions above.


Optional extra
==============

  If you have a project management website you should seriously
  consider installing the ``xm.theme`` package.  This gets rid of part
  of the default Plone UI so it fits a project management site more.
  Try this out locally before you use it in production.  Note that
  this may become a real dependency in newer versions of
  Products.eXtremeManagement


Conflicting Products
====================

  * eXtremeManagement is known not to work with ZEPP/PlonePM, another
    project management product.  It uses a Task content type, just
    like eXtremeManagement does.  This causes problems.  If you want
    to try out both, do that in separate Zope instances.

  * Same is true for PloneBooking.
