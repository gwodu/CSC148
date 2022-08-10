"""Assignment 2 - Priority Queue [Task 3]

CSC148, Summer 2021

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

This module is adapted from the Winter 2021 A1, created by Diane
Horton, Ian Berlott-Attwell, Jonathan Calver, Sophia Huynh, Maryam
Majedi, and Jaisie Sin.

Adapted by: Saima Ali and Marina Tawfik

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 the Department of Computer Science,
University of Toronto

===== Module Description =====

This module contains the Container, _QueueNode, and PriorityQueue classes.
"""
from __future__ import annotations
from typing import Any, Callable, Optional, Tuple


class Container:
    """A container that holds Objects.

    This is an abstract class.  Only child classes should be instantiated.
    """

    def add(self, val: Any) -> None:
        """Add <item> to this Container.
        """
        raise NotImplementedError

    def remove(self) -> Any:
        """Remove and return a single item from this Container.
        """
        raise NotImplementedError

    def is_empty(self) -> bool:
        """Return True iff this Container is empty.
        """
        raise NotImplementedError


# Used in the doctest examples for PriorityQueue
def _shorter(a: Any, b: Any) -> bool:
    """
    Return True if the length of <a>
    is shorter than that of <b>.

    Preconditions:
    - type(a) == type(b)
    - The types of <a> and <b> are such that len(a)
      and len(b) are valid operations
    """
    return len(a) < len(b)


class _QueueNode:
    """A _QueueNode that represents an item in a Queue.

    === Public Attributes ===
    val:
      The value of the _QueueNode. This could represent a job to be completed.

    next:
      The _QueueNode with the next-highest priority. The convention used is that
      priority 1 is the highest possible priority, and if q.next == v, where
      v is a _QueueNode, (priority of v) = (priority of q) + 1.

      If next is None, the _QueueNode is at the end of the Queue, or is not
      part of any Queue.

    === Representation Invariants ===
    - for any _QueueNode, q, if q.next is not None, then
      type(q.next.val) == type(q.val)
    - for any _QueueNode, q, calling q = q.next repeatedly
      will yield q is None after a finite number of calls.
    """
    val: Any
    next: Optional[_QueueNode]

    def __init__(
            self, val: Any,
            next_node: Optional[_QueueNode] = None
    ) -> None:
        """Initializes a new QueueNode with val <val> and
        <next> set to <next_node>.

        >>> q = _QueueNode("llama")
        >>> q.val
        'llama'
        >>> q.next is None
        True
        >>> p = _QueueNode(1)
        >>> n = _QueueNode(2, p)
        >>> n.next is p
        True
        >>> n.val
        2
        >>> p.val
        1
        """
        self.val = val
        self.next = next_node

    def __str__(self) -> str:
        """Return the string representation for this _QueueNode.
        """
        return f"_QueueNode with value {self.val}"


class PriorityQueue(Container):
    """A queue of items that operates in FIFO-priority order.

    Items are removed from the queue according to priority; the item with the
    highest priority is removed first.  Ties are resolved in first-in-first-out
    (FIFO) order, meaning the item which was inserted *earlier* is the first one
    to be removed.

    Priority is defined by the <higher_priority> function that is provided at
    time of initialization.

    _first:
      The _QueueNode representing the Queue element with the highest priority.
    _higher_priority:
      A function that compares two items by their priority.
      If _higher_priority(x, y) is true, then x has higher priority than y
      and should be inserted in the queue before y.

    === Representation Invariants ===
    - _first.val matches the type required as per the input arguments for the
      function _higher_priority.
    - _higher_priority takes two arguments of the same type
    - the structure of _first always obeys the priority dictated by
      _higher_priority, such that
      _higher_priority(_first.val, _first.next.val) == True
    - _first is None if and only if the PriorityQueue is empty.
    """
    _first: Optional[_QueueNode]
    _higher_priority: Callable[[Any, Any], bool]

    def __init__(
            self, higher_priority: Callable[[Any, Any], bool]
    ) -> None:
        """Initialize an empty PriorityQueue.

        >>> pq = PriorityQueue(str.__lt__)
        >>> pq.is_empty()
        True
        """
        self._first = None
        self._higher_priority = higher_priority

    def _get_prev_last(self) -> Optional[Tuple[_QueueNode]]:
        """Return the second to the last node on the Queue"""
        curr = self._first

        if curr is None:
            return None
        if curr.next is None:
            return curr

        while curr.next.next is not None:
            curr = curr.next
        return curr

    def _get_last(self) -> Optional[Tuple[_QueueNode]]:
        """Return the last _Queuenode in the Priority Queue, or return None
        if the Queue is empty
        >>> pq = PriorityQueue(str.__lt__)
        >>> pq._get_last() is None
        True
        >>> val = "Gamma"
        >>> pq.add(val)
        >>> pq._get_last().val == "Gamma"
        True
        """

        curr = self._first

        if curr is None:
            return None

        while curr.next is not None:
            curr = curr.next
        return curr

    def add(self, val: Any) -> None:
        """Add a value <val> to this PriorityQueue.

        >>> pq = PriorityQueue(_shorter)
        >>> pq.is_empty()
        True
        >>> val = "Gamma"
        >>> pq.add(val)
        >>> pq.is_empty()
        False
        >>> pq._first.val
        'Gamma'
        >>> pq._first.next is None
        True
        >>> pq.add("Beta")
        >>> pq._first.val
        'Beta'
        >>> pq._first.next.val
        'Gamma'
        >>> pq._first.next.next is None
        True
        """
        new_node = _QueueNode(val)
        # prev_last_node = self._get_prev_last()
        # last_node = self._get_last()

        if self._first is None:  # if the list is empty
            self._first = new_node
        curr = self._first  # curr is assigned first item in queue

        # makes new_node first item in queue if it's a higher priority
        if self._higher_priority(new_node.val, self._first.val):
            self._first, new_node.next = new_node, self._first
        else:
            # add new_node after curr and remove it if that's not it's final
            # destination
            while curr is not None and \
                    not self._higher_priority(new_node.val, curr.val):
                curr_node = curr
                next_node = curr.next
                curr.next, new_node.next = new_node, curr.next
                curr = new_node.next
                if next_node is not None and not\
                        self._higher_priority(new_node.val, next_node.val):
                    curr_node.next = next_node

    def remove(self) -> Any:
        """Remove and return the next value from this PriorityQueue.

        Precondition: this priority queue is non-empty.

        >>> pq = PriorityQueue(_shorter)
        >>> pq.add("Delta")
        >>> pq.add("Beta")
        >>> pq.add("Epsilon")
        >>> pq.add("Alpha")
        >>> q = pq.remove()
        >>> q == "Beta"
        True
        >>> q = pq.remove()
        >>> q == "Delta"
        True
        >>> q = pq.remove()
        >>> q == "Alpha"
        True
        >>> q = pq.remove()
        >>> q == "Epsilon"
        True
        """
        first = self._first
        self._first = first.next
        return first.val

    def is_empty(self) -> bool:
        """Return True iff this PriorityQueue is empty.

        >>> pq = PriorityQueue(str.__lt__)
        >>> pq.is_empty()
        True
        >>> pq.add("Llama")
        >>> pq.is_empty()
        False
        """
        return self._first is None

    def get_priority(self, val: Any) -> int:
        """Get the priority of <node> in the PriorityQueue.

        The QueueNode self._first is priority 1. See the
        class-level description for QueueNode for details
        on the convention for priority.

        If <node> is not in the PriorityQueue, return -1.

        >>> pq = PriorityQueue(_shorter)
        >>> pq.add("Delta")
        >>> pq.add("Beta")
        >>> pq.add("Epsilon")
        >>> pq.add("Alpha")
        >>> pq.get_priority("Beta")
        1
        >>> pq.get_priority("Delta")
        2
        >>> pq.get_priority("Alpha")
        3
        >>> pq.get_priority("Epsilon")
        4
        """
        if self._first.val == val:
            return 1
        else:
            priority = 1
            curr_node = self._first

            while curr_node is not None:
                if curr_node.val == val:
                    return priority
                else:
                    priority += 1
                    curr_node = curr_node.next

            return -1

    def __str__(self) -> str:
        """Return a string representation of this PriorityQueue.
        >>> pq = PriorityQueue(_shorter)
        >>> pq.add("Delta")
        >>> pq.add("Beta")
        >>> pq.add("Epsilon")
        >>> pq.add("Alpha")
        >>> print(pq)
        Beta -> Delta -> Alpha -> Epsilon
        """
        str_queue = f"{self._first.val}"
        curr = self._first.next
        while curr is not None:
            str_queue += f" -> {curr.val}"
            curr = curr.next

        return str_queue

        # You will not be graded on your string representation,
        # but it may be helpful when debugging.


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': ['doctest', 'python_ta',
                                   'typing', '__future__'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })

    import doctest
    doctest.testmod()
