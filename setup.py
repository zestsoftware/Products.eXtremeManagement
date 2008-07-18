from setuptools import setup, find_packages
import os

versionfile = open(os.path.join('Products', 'eXtremeManagement', 'version.txt'))
version = versionfile.read().strip()
versionfile.close()

setup(name='Products.eXtremeManagement',
      version=version,
      description="Project administration which supports the eXtreme Programming Methodology.",
      long_description="""\
eXtreme Management Tool
=======================


Features
--------

This application provides project administration which supports the
eXtreme Programming Methodology.  By developing a number of new
content types we can use iterations, Stories and tasks to manage our
XP projects.


Content Types
-------------

    * Project
      Multiple projects can be added by employees. For each project
      contact information of team members, iterations and stories can
      be added by both the customers and employees.

    * Iteration
      The project will be planned with iterations. An iteration is a
      period of 2 to 4 weeks in which a number of stories will be
      implemented.

    * Offer
      Contains the stories that a customer wants in this Project. It
      is used as a way to bundle the wishes of the client and give a
      first indication of the size of a project.

    * Story
      The customer can define new features by describing these feature
      in a story.

    * Task
      The employees can estimate the story by defining tasks.


Workflow
--------

Customers can create stories and submit them for estimating. The
employees will find pending stories in the review portlet and can
start adding more detailed tasks.

After the employee has finished reviewing the story and giving it a
rough estimate, he can set the estimate transition.  The customer can
then move the story to the preferred iteration.

Of course this can be done with customer and employees together during
an iteration meeting.  In most cases: anything that the customer can
do, the employee can do as well.  A Manager can do anything.

After the stories are assigned to the iteration, the state of the
iteration can be set to 'active'. Now employees can book their working
hours on the tasks as the project goes on.


Time Registration
-----------------

When a developer has done work on a task he can add bookings to the
task and describe the work in the comment field.


Project overview
----------------

Customers can monitor all progress at the project overview page. This
gives the customer the "Overall Plan" by showing each iteration in a
list with progress bars. By clicking on an iteration more detailed
information will be shown about the stories.
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
	  'Products.contentmigration == 1.0b4',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
