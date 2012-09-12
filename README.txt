eXtreme Management Tool
=======================

This application provides project administration which supports the
eXtreme Programming Methodology.

Content Types
-------------

    * Project
      Multiple projects can be added by projectmanagers. For each project,
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

Customers can create stories and submit them for estimating. The employees
will find pending stories in the review portlet and provide a rough estimate
and change the state by using the 'mark estimated' transition.

The customers are able to prioritize the stories based on value for the
organisation and the rough estimate. When the team has committed to the number
of stories, they can start writing tasks and provide estimates for each task.

After all tasks have been written and estimated the iteration can be
started by following the transition 'start working'. This will set the status
of all tasks to 'todo', so employees will see their tasks in the todo list.

Activating tasks will send notification email to the assignees. When
an iteration is activated, this could result in quite some mails to be
sent. To prevent this from slowing down the activation of the
iteration, one could consider adding MaildropHost in the instance.

When completing all tasks in a story the story itself will be set to
'completed'.


Time Tracker
------------

The time tracker allows the employees to track their work in real time. You
can select a few tasks to work on from the list of assigned tasks. The tracker
will display an input field for each task. Instead of using the punch-in,
punch-out system we choose to start working by just starting the timer. After
you have finished a task you describe your work in the input field and hit the
'track' button

The time spent on the task will be registered with your description and the
timer will reset itself so you can start on the next task.

In case you get interrupted by a phone call or a colleague asking for help,
you simply provide a quick note on what you were doing in the task input.
Again this will reset the timer. At the bottom of the tracker an input field
for unassigned tasks is available, to track interruptions like these. If you
register the time here, you can later hit the 'Add to task' button, which
allows you to browse through all open tasks and book the time there.

At the end of the day you can expand each task do any last changes to either
the description or the time. In case you didn't finish the task yet you can
click the 'book' button to add a booking to the task with the total time. When
you did finish the task you can click 'book and close', this will change the
state of the task to completed.


Release Plan
------------

The Release Plan provides the customer with an "Overall Plan". At the start of
a project all stories are added to the project. Depending on the velocity of
the development team and the size and number of stories the expected number of
iterations can be added. The customer can than prioritize the user stories using
drag and drop and assign them to iterations.


Iteration Roundup
-----------------

When the iteration is finished, some stories might not be completed. Using the
close iteration option from the 'action' dropdown allows you to select or
create the next iteration and copy over all unfinished stories, including
unfinished tasks.

