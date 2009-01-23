eXtreme Management Tool
=======================


Features
--------

This application provides project administration which supports the
eXtreme Programming Methodology.

Content Types
-------------

    * Project
      Multiple projects can be added by employees. For each project,
      iterations and stories can be added by both the customers and employees.

    * Iteration
      The project will be planned with iterations. An iteration is a
      period of 1 to 3 weeks in which a number of stories will be
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

    * Booking
      While working on tasks the employees can track time and easily book
      those at the end of the day.


Workflow
--------

Customers can create stories and submit them for estimating. The
employees will find pending stories in the review portlet. He will fill-in a
rough estimate and change the state by using the 'mark estimated' transition.

The customers are able to prioritize the stories based on value for the
organisation and the rough estimate. When the team has committed to the number
of stories, they can start writing tasks and provide estimates for each task.

After all tasks have been written and estimated the iteration can be
started by following the transition 'start working'. This will set the status
of all tasks to 'todo', so developers will see their tasks in the todo list.

(Activating tasks will send notification email to the assignees. When
an iteration is activated, this could result in quite some mails to be
sent. To prevent this from slowing down the activation of the
iteration, one could consider adding MaildropHost in the instance.)

When completing all tasks in a story the story itself will be set to
'completed'.


Time Registration
-----------------

When a developer has done work on a task he can add bookings to the
task and describe the work in the comment field.


Project overview
----------------

Customers can monitor all progress at the Iteration overview page. This
gives the customer the "Overall Plan" by showing each iteration in a
list with progress bars. By clicking on an iteration more detailed
information will be shown about the stories.
