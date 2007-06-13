python = 'python2.4'
zope_version = '2.9.7'

symlink_sources = [
    'eXtremeManagement',
    ]
symlink_basedir_template = '%(user_dir)s/svn'
archive_sources = [
    {'source': 'FCKeditor.Plone-2.3.2.tar.gz',
     'url': 'http://surfnet.dl.sourceforge.net/sourceforge/fckeditor/FCKeditor.Plone-2.3.2.tar.gz',
     },
    {'url': 'http://codespeak.net/z3/five/release/Five-1.4.2.tgz'},
    ]
symlinkbundle_sources = [
    {'source': 'plone25-zope29',
     'url': 'http://svn.plone.org/svn/plone/bundles/2.5-zope29'
     },
    {'source': 'Poibundle',
     'url': 'http://svn.plone.org/svn/collective/Poi/bundles/trunk',
     },
    {'source': 'plone25develop',
     'develop': True,
     'url': 'https://svn.plone.org/svn/collective/developerconfig/bundles/plone25develop',
     },
    ]
archivebundle_sources = [
    ]
plone_site_name = 'projects.zestsoftware.nl'
main_products = ['eXtremeManagement',
                 {'source': 'developerconfig',
                  'develop': True},
                 ]
