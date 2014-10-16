from setuptools import setup, find_packages

readme = open('README.txt').read().strip()
install = open('INSTALL.txt').read().strip()
authors = open('AUTHORS.txt').read().strip()
history = open('CHANGES.rst').read().strip()

long_description = (
    readme + '\n\n' + install + '\n\n' + authors + '\n\n' + history)

setup(name='Products.eXtremeManagement',
      version='2.1a9',
      description="Project administration which supports the eXtreme Programming methodology.",
      long_description=long_description,
      classifiers=[
          "Framework :: Plone",
          "Framework :: Plone :: 3.3",
          "Framework :: Plone :: 4.0",
          "Framework :: Plone :: 4.1",
          "Framework :: Plone :: 4.2",
          "Framework :: Zope2",
          "Framework :: Zope3",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.4",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Topic :: Software Development :: Libraries :: Python Modules",
          ],
      keywords='',
      author='Zest Software',
      author_email='info@zestsoftware.nl',
      url='http://plone.org/products/extreme-management-tool',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'xm.booking',
          'xm.portlets',
          'xm.tracker',
          'xm.charting',
          'kss.plugin.yuidnd',
          'kss.plugin.cns',
          'Products.contentmigration >= 1.0b4',
          'Products.Poi',
          'pygooglechart',
          'collective.autopermission',
          'zope.app.content',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
