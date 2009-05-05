from setuptools import setup, find_packages
import os


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = read('Products', 'eXtremeManagement', 'version.txt').strip()
readme = read('Products', 'eXtremeManagement', 'README.txt')
install = read('Products', 'eXtremeManagement', 'INSTALL.txt')
authors = read('Products', 'eXtremeManagement', 'AUTHORS.txt')
history = read('Products', 'eXtremeManagement', 'HISTORY.txt')

long_description = readme + '\n\n' + install + '\n\n' + authors
long_description += '\n\n' + history


setup(name='Products.eXtremeManagement',
      version=version,
      description="Project administration which supports the eXtreme Programming methodology.",
      long_description=long_description,
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
          'xm.booking >= 1.0, <= 1.1dev',
          'xm.portlets >= 0.8, <= 0.9dev',
          'xm.tracker >= 1.0, <= 1.1dev',
          'xm.charting >= 0.3, <= 0.4dev',
          'kss.plugin.yuidnd >= 0.7, <= 0.8dev',
          'kss.plugin.cns >= 1.1, <= 1.2dev',
          'Products.contentmigration >= 1.0b4',
          'Products.Poi >= 1.2, <= 1.3dev',
          'pygooglechart >= 0.2.1, <= 0.3dev',
          'collective.autopermission',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
