"""
Question 4 [10 marks]

Below is the LinkedList class we have worked on in this course, with just
the parts you need to answer this question.

(a) We have added new method chop_front, but parts are missing. Replace each
"XXX" to complete this method according to its docstring. Add code only where
indicated by "XXX", and do not change any of the existing code. Complete the
"we know that" comment with whatever we can infer must be true about the
variables.

(b) Write a pytest that tests for this part of the specification:
"If n > the length of this linked list, remove all the nodes."
"""

from __future__ import annotations
from typing import Any, Optional


class _Node:
    """A node in a linked list.

    Note that this is considered a "private class", one which is only meant
    to be used in this module by the LinkedList class, but not by client code.

    === Attributes ===
    item:
        The data stored in this node.
    next:
        The next node in the list, or None if there are no more nodes.
    """
    item: Any
    next: Optional[_Node]

    def __init__(self, item: Any) -> None:
        """Initialize a new node storing <item>, with no next node.
        """
        self.item = item
        self.next = None  # Initially pointing to nothing


class LinkedList:
    """A linked list implementation of the List ADT.

    === Private Attributes ===
    _first:
        The first node in the linked list, or None if the list is empty.
    """
    _first: Optional[_Node]

    def __init__(self, items: list) -> None:
        """Initialize a new linked list containing the given items.

        The first node in the linked list contains the first item
        in <items>.
        """
        if items == []:  # No items, and an empty list!
            self._first = None
        else:
            self._first = _Node(items[0])
            curr = self._first
            for item in items[1:]:
                curr.next = _Node(item)
                curr = curr.next

    def is_empty(self) -> bool:
        """Return whether this linked list is empty.

        >>> LinkedList([]).is_empty()
        True
        >>> LinkedList([1, 2, 3]).is_empty()
        False
        """
        return self._first is None

    def __str__(self) -> str:
        """Return a string representation of this list in the form
        '[item1 -> item2 -> ... -> item-n]'.

        >>> str(LinkedList([1, 2, 3]))
        '[1 -> 2 -> 3]'
        >>> str(LinkedList([]))
        '[]'
        """
        items = []
        curr = self._first
        while curr is not None:
            items.append(str(curr.item))
            curr = curr.next
        return '[' + ' -> '.join(items) + ']'

    def chop_front(self, n: int) -> int:
        """Remove the first n nodes from this linked list, if possible.
        If n > the length of this linked list, remove all the nodes.

        Return the number of nodes that were removed.

        precondition: n >= 1

        >>> linky = LinkedList([1, 2, 3, 4, 5, 6, 7, 8])
        >>> linky.chop_front(3)
        3
        >>> print(linky)
        [4 -> 5 -> 6 -> 7 -> 8]
        >>> linky = LinkedList([22, 1, 5, 4, 7, 4])
        >>> linky.chop_front(13)
        6
        >>> print(linky)
        []
        >>> linky = LinkedList([1, 2, 3, 4, 5])
        >>> linky.chop_front(8)
        5
        >>> print(linky)
        []
        """
        if self.is_empty():
            return 0
        else:
            curr = self._first
            i = 0
            while curr.next is not None and i < n - 1:
                curr = curr.next
                i += 1
            # We know that: curr is either the nth element in the list, or
            # curr is the last element

            # Add below whatever is needed to complete the method.
            self._first = curr.next
            return i + 1



