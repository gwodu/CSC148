"""
Question 1 [8 marks]

Here's the start of some code for managing rooms in the department of Computer
Science. It has a problem: When run, an error is raised.

(a) Draw a memory model diagram that shows the state of memory immediately
before the print statement in the main block. If any stack frames are popped
prior to this moment, just cross them out rather than erase them.

You may draw your answer by hand. Scan it or take a photograph of it, and submit
it to MarkUs in a file called Q1a.extension, where extension is pdf,
png, HEIC, or whatever format your phone or scanner produces.

(b) Correct the code so that this error is not raised. Do not correct or improve
anything else; just ensure that the code runs without raising an error.

(c) Suppose we consider two meeting rooms to be equivalent iff they seat the
same number of people. Modify the code so that we can compare meeting rooms as
shown in the __main__ block.
"""
from __future__ import annotations
from typing import List


class Room:
    """
    === Public Attributes ===
    users: the names of people who have key access to this Room.
    """
    users: List[str]

    def __init__(self) -> None:
        self.users = []


class Office(Room):
    """
    === Public Attributes ===
    users: the names of people who have key access to this Room.
    owner: the name of the person whose office this is
    bookshelves: the number of bookshelves in this office
    """
    owner: str
    bookshelves: int

    def __init__(self, owner: str, shelves: int) -> None:
        self.owner = owner
        self.bookshelves = shelves
        Room.__init__(self)

class MeetingRoom(Room):
    """
    === Public Attributes ===
    users: the names of people who have key access to this Room.
    capacity: the number of people this room can seat.
    """
    capacity: int

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity

    def __eq__(self, other: MeetingRoom):
        return self.capacity == other.capacity

if __name__ == '__main__':
    ba4260 = Office('Campbell', 3)
    # Memory model diagram is for this moment.
    print(ba4260)
    if len(ba4260.users) == 0:
        print('currently no one has card access')
    ba4290 = MeetingRoom(18)
    ba4242 = MeetingRoom(8)
    if ba4290 == ba4242:
        print('equivalent rooms')
