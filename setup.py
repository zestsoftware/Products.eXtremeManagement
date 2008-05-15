from setuptools import setup, find_packages
import os

versionfile = open(os.path.join('Products', 'eXtremeManagement', 'version.txt'))
version = versionfile.read().strip()
versionfile.close()

setup(name='Products.eXtremeManagement',
      version=version,
      description="",
      long_description="""\
""",
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
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
