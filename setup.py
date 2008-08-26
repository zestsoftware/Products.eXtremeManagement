from setuptools import setup, find_packages
import os

versionfile = open(os.path.join('Products', 'eXtremeManagement', 'version.txt'))
version = versionfile.read().strip()
versionfile.close()

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(name='Products.eXtremeManagement',
      version=version,
      description="Project administration which supports the eXtreme Programming Methodology.",
      long_description=(
      read('Products', 'eXtremeManagement', 'README.txt')
      + '\n' +
      'AUTHORS\n'
      '=======\n'
      + '\n' + read('Products', 'eXtremeManagement', 'AUTHORS.txt')
      + '\n' +
      'HISTORY\n'
      '=======\n'
      + '\n' +
      read('Products', 'eXtremeManagement', 'HISTORY.txt')
      ),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Framework :: Zope3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Zest Software',
      author_email='xm@lists.zestsoftware.nl',
      url='http://plone.org/products/extreme-management-tool',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'xm.booking',
          'xm.portlets',
          'xm.charting',
          'kss.plugin.yuidnd',
          'Products.contentmigration == 1.0b4',
          'Products.Poi',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
