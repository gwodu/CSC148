""" CSC148 Summer 2021 Term Test 2

Q3: Linked Lists [25 marks]
-----------------------------------------------------------------------------

Write pytest test cases that will fail on incorrect implementations
of the method LinkedList.merge(). We have included a working version of this
method below, as well as the _Node class and everything you need from the
LinkedList class.

You are guaranteed that any buggy implementation of LinkedList.merge()
will be passed inputs that obey and return values that obey the type
annotations.

Your tests should verify that the values is this LinkedList has been modified
correctly. You do NOT need to check that self has been modified in place
or if other has not been modified.

A syntax checker is available to you on MarkUs that only checks that your code
doesn't throw a syntax error i.e. it does NOT check for correctness.

Guidelines:
- Make sure you give each test function a unique name!
- You do NOT have to write docstrings for your tests or provide type
  annotations.
- Do NOT add new imports.
- Do NOT add to or alter the LinkedList class or the _Node class.
"""
from __future__ import annotations

from typing import Any, Optional
import pytest


################################################################################
# Here is an example test case.  Add your test cases below it.
################################################################################
def test_doctest():
    """A test case matching the doctest in LinkedList.merge.
    """
    my_list = LinkedList([1, 3, 5])
    my_list.merge(LinkedList([2, 4, 6]))

    assert my_list == LinkedList([1, 2, 3, 4, 5, 6])

def test_empty_list():
    my_list = LinkedList([])
    my_list.merge(LinkedList([]))

    assert my_list == LinkedList([])

def test_single():
    my_list = LinkedList([1])
    my_list.merge(LinkedList([2]))

    assert my_list == LinkedList([1, 2])

def test_empty_single():
    my_list = LinkedList([])
    my_list.merge(LinkedList([2]))

    assert my_list == LinkedList([2])

def test_sinlge_empty():
    my_list = LinkedList([5])
    my_list.merge(LinkedList([]))

    assert my_list == LinkedList([5])

def test_short_no_sort():
    my_list = LinkedList([1, 2, 3])
    my_list.merge(LinkedList([4, 5, 6]))

    assert my_list == LinkedList([1, 2, 3, 4, 5, 6])

def test_mid_sort():
    my_list = LinkedList([1, 3, 4, 9, 11, 12])
    my_list.merge(LinkedList([2, 5, 6, 8, 10, 13]))

    assert my_list == LinkedList([1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13])

def test_mid_no_sort():
    my_list = LinkedList([1, 2, 3, 4, 5, 6])
    my_list.merge(LinkedList([8, 9, 10, 11, 12, 13]))

    assert my_list == LinkedList([1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13])

def test_long_no_sort():
    my_list = LinkedList([1, 2, 3, 4, 5, 6, 7, 8 , 9 , 10, 11, 12, 13])
    my_list.merge(LinkedList([14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]))

    assert my_list == LinkedList([1, 2, 3, 4, 5, 6, 7, 8 , 9 , 10, 11, 12, 13,
                                  14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26])

def test_long_sort():
    my_list = LinkedList([1, 2, 4, 5, 6, 8 , 9 , 11, 12, 15, 18, 21, 25])
    my_list.merge(LinkedList([3, 7, 10, 13, 14, 16, 17, 19, 20, 22, 23, 24, 26]))

    assert my_list == LinkedList([1, 2, 3, 4, 5, 6, 7, 8 , 9 , 10, 11, 12, 13,
                                  14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26])

def test_dif_length():
    my_list = LinkedList([1, 3, 4,])
    my_list.merge(LinkedList([2, 5, 6, 8, 9, 10, 11, 12, 13]))

def test_dif_length():
    my_list = LinkedList([2, 5, 6, 8, 9, 10, 11, 12, 13])
    my_list.merge(LinkedList([1, 3, 4]))

    assert my_list == LinkedList([1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13])

def test_repetition():
    my_list = LinkedList([2, 2, 5, 6, 6, 8, 9, 10, 11, 11, 12, 13])
    my_list.merge(LinkedList([1, 3, 4, 7, 7]))

    assert my_list == LinkedList([1, 2, 2, 3, 4, 5, 6, 6, 7, 7, 8, 9, 10, 11, 11, 12, 13])

################################################################################
# Below is the LinkedList class and the method you are testing. For your
# convenience, we have moved the definition of that method to the top of the
# class. _Node is defined at the very bottom of this file.
################################################################################
class LinkedList:
    """A linked list implementation of the List ADT.

    === Private Attributes ===
    _first:
        The first node in the linked list, or None if the list is empty.
    """
    _first: Optional[_Node]

    def __init__(self, items: list) -> None:
        """Initialize a new linked list containing the given items, in the
        same order as <items>.

        The first node in the linked list contains the first item in <items>.
        """

        # This method is provided for you. Do NOT change it.

        if len(items) == 0:  # No items, and an empty list!
            self._first = None
        else:
            self._first = _Node(items[0])
            curr = self._first
            for item in items[1:]:
                curr.next = _Node(item)
                curr = curr.next

    def __str__(self) -> str:
        """Return a string representation of this list in the form
        '[item1 -> item2 -> ... -> item-n]'.

        >>> str(LinkedList([1, 2, 3]))
        '[1 -> 2 -> 3]'
        >>> str(LinkedList([]))
        '[]'
        """

        # This method is provided for you. Do NOT change it.

        items = []
        curr = self._first
        while curr is not None:
            items.append(str(curr.item))
            curr = curr.next
        return '[' + ' -> '.join(items) + ']'

    def __eq__(self, other: LinkedList) -> bool:
        """Return True if this LinkedList include the same values in the same
        order as <other>
        """

        # This method is provided for you. Do NOT change it.

        curr_node, other_node = self._first, other._first
        while curr_node and other_node:
            if curr_node.item != other_node.item:
                return False

            curr_node, other_node = curr_node.next, other_node.next

        return curr_node == other_node

    def merge(self, other: LinkedList) -> None:
        """Merge the values in <other> into this sorted LinkedList.

        Precondition: this LinkedList and <other> include numbers only and
        both are sorted in non-descending order.

        >>> my_list = LinkedList([1, 3, 5])
        >>> my_list.merge(LinkedList([2, 4, 6]))
        >>> print(my_list)
        [1 -> 2 -> 3 -> 4 -> 5 -> 6]
        """
        prev_node, curr_node, other_node = None, self._first, other._first

        while other_node:
            new_node = None
            if curr_node and (curr_node.item <= other_node.item):
                prev_node, curr_node = curr_node, curr_node.next
            else:
                new_node = _Node(other_node.item)

            if new_node:
                other_node = other_node.next
                if prev_node:
                    prev_node.next = new_node
                    new_node.next = curr_node
                else:
                    new_node.next = self._first
                    self._first = new_node

                prev_node = new_node


class _Node:
    """A node in a linked list.

    === Attributes ===
    item:
        The data stored in this node.
    next:
        The next node in the list, or None if there are no subsequent nodes.
    """
    item: Any
    next: Optional[_Node]

    def __init__(self, item: Any) -> None:
        """Initialize a new node storing <item>, with no next node.
        """

        # This method is provided for you. Do NOT change it.

        self.item = item
        self.next = None  # Initially pointing to nothing


if __name__ == '__main__':
    # The line below runs pytest on the current file, regardless of its name.
    # Do NOT change that line.
    pytest.main([__file__])
