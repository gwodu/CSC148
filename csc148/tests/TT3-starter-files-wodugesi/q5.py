""" CSC148 Summer 2021 Term Test 3

Q5: Object Oriented Programming & Class Design [25 marks]
-----------------------------------------------------------------------------

You are creating a **Task Manager** to manage the resources of a
custom operating system. Your operating system keeps track of time in
the unit of clock cycles.

=== TASK MANAGER =========================================================
| Must support the following operations:                                 |
|   ▶ Record processes which have requested resources, in FIFO order     |   -> Queue
|   ▶ Keep track of the processes that are currently running             |
|   ▶ Keep track of completed processes                                  |
|   ▶ Execute (in LIFO order) as many processes as possible within       |   -> Stack
|     a defined memory limit                                             |
|   ▶ Keep track of elapsed clock cycles                                 |
==========================================================================

There are (2) types of tasks you need to consider, described below:
File R/W, and Render. In the future, you may need to expand to handle
other types of tasks. Each task occupies a constant amount of memory
during the time it runs.

===========================================================================
| TASK TYPE    | DESCRIPTION                                              |
===========================================================================
| File R/W     | Invoked when the system is asked to access (read) the    |
|              | contents of a file, or write contents to a file.         |
|              | ▶ For a file of size <n> bytes:                          |
|              |    - A file read takes <n> * 2 clock cycles to complete  |
|              |    - A file write takes <n> clock cycles to complete     |
|              |    - The process requires <n> bytes of memory            |
|--------------------------------------------------------------------------
| Render       | Invoked when the system is asked to render images or     |
|              | video content.                                           |
|              | ▶ Requires <byte-rate> bytes per clock cycle.            |
|              | ▶ Runs for <duration> clock cycles                       |
|              | ▶ <byte-rate> and <duration> are fixed within the        |
|              |   process & vary across different render processes       |
===========================================================================

(i) [20 marks] For the above application, write the class initializers for
each of the required classes. You don't need to write any other methods.
You will need to design these classes yourself and identify
any inheritance and/or composition relationships.

You do not need to write docstring examples.

Additional requirements:
  - You must include type annotations for the class instance attributes and
    method headers.
  - You must include descriptions of each of the class attributes (you can do
    this in the docstring or as comments throughout the initializer)
  - You must create attributes with meaningful names that are descriptive of
    what they represent.
  - Do **NOT** add any import statements other than from the typing module. You
    may remove imports that you do not need.

(ii) [5 marks] In your own words, explain the difference between composition
and inheritance in the context of object oriented programming. Give an
example for each from the classes you designed in part (i).

If you did not use composition and/or inheritance, explain why you decided they
were not suitable for the application.

    TODO: part (ii)
    COMPOSition is when an attribute of one class is an instance of another class. while inheritance
    occurs when a class inherits the attributes and instances of another class.
    Composition TaskManager has a List of Tasks
    Composition: Read and Write inherit the initialiser and attributes of File

A syntax checker is available to you on MarkUs. It is only for syntax errors
i.e. it does NOT check for correctness.
"""

from __future__ import annotations
from typing import List, Any, Optional, Dict

# TODO: part (i), define your classes and their initializers here
class TaskManager():
    """A Task Manager Class
    tasks: a list of processes that have requested resources. It will contain no
                process that is running or has been completed. If a process is running or
                being completed, it will be removed and appended to either processing or completed
    processing: a list of processes that are currently being run
    completed: a list of process that have been completed
    free_memory: the amount of memory the Operating System has available for running tasks.
    memory_being_used: the amount of memory that is currently being used to run tasks
    total_memory: the total amount of memory the OS has. free_memory + memory_being_used = total_memory
    clock_cycles: to keep track of time that has been elapsed. Every time each task is run, the time
                    attribute is increased by the amount of time the task took.
    """
    tasks : List[Dict[Task, str]]
    processing : List[Task]
    completed : List[Task]
    total_memory: int
    memory_being_used: int
    free_memory: int
    clock_cycles: int

    def __init__(self, tasks, total_memory):
        """Initialises an instance of class Task Manager"""
        self.tasks = tasks
        self.total_memory = total_memory
        self.processing = []
        self.completed = []
        self.memory_being_used = 0
        self.free_memory = 0
        self.clock_cycles = 0

    class Task:
        """A Task Class"""

        def __init__(self):
            raise NotImplementedError

    class File(Task):
        """A File Class
        size: the size of the file and how much memory it takes to run
        """
        size: int

        def __init__(self, size: int):
            self.size = size

    class Read(File):
        """A Read Task class
        time: the time it takes"""
        time: int

        def __init__(self, size: int):
            File.__init__(self, size)
            self.time = size * 2

    class Write(File):
        """A Read Task class
        time: the time it takes"""
        time: int

        def __init__(self, size: int):
            File.__init__(self, size)
            self.time = size

    class Render(Task):
        """A Render class"""
        def __init__(self):
            raise NotImplementedError

    class ImageRender(Render):
        """A VideoRender class
        byterate: Bytes per clock cycle
        duration: the time it takes to run"""
        byterate: float
        duration: float


        def __init__(self) -> None:
            self.byterate = byterate # byterate and duration are given values by constants
            self.duration = duration

    class VideoRender(Render):
        """A VideoRender class
        byterate: Bytes per clock cycle
        duration: the time it takes to run"""

        byterate: float
        duration: float

        def __init__(self, byterate, duration) -> None:
            self.byterate = byterate
            self.duration = duration # byterate and duration are given values by constants
