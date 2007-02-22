# -*- coding: utf-8 -*-

from zope.interface import Interface


class IXMCustomerFolder(Interface):
    """eXtremeManagement CustomerFolder

    Normal Folder that can only contain Customers.
    """


class IXMCustomer(Interface):
    """eXtremeManagement Customer

    Folder describing one customer (think of a company).

    This Folder can contain ProjectMembers.
    """


class IXMProjectMember(Interface):
    """eXtremeManagement ProjectMember

    Some basic information about project members.  A project member is
    usually a contact person of the customer or an employee of the
    development company.
    """


class IXMProjectFolder(Interface):
    """eXtremeManagement ProjectFolder

    Normal Folder that can only contain Projects.
    """


class IXMProject(Interface):
    """eXtremeManagement Project

    Folder where you add information about a project.  In Extreme
    Programming terms this can also function as a Release.

    A Project can at least contain Iterations.
    """


class IXMIteration(Interface):
    """eXtremeManagement Iteration

    An Iteration is usually a period of a few weeks.  During that
    Iteration you implement some Stories for the customer.

    So an Iteration can contain Stories.
    """


class IXMStory(Interface):
    """eXtremeManagement Story

    A Story is a feature or a coherent set of features that together
    tell a story that the customer wants implemented.  This Story
    should not be bigger than a few days.

    A Story contains Tasks.  When all Tasks are finished, the Story
    should be finished as well.
    """


class IXMTask(Interface):
    """eXtremeManagement Task

    A Task is a subset of a Story.  It can be assigned to one or more
    employees.  A Task should not take more than one day.

    A Task contains Bookings.
    """


class IXMBooking(Interface):
    """eXtremeManagement Booking

    A Booking is made by an employee to show that he did some work on
    a Task.  Add all Bookings and you know how long the Task (and its
    parent Story and parent Iteration) actually took.  This can be
    used to bill the customer.

    A Booking contains no other content types.  Next to ProjectMember
    it is the only non-folderish content type we define.
    """
