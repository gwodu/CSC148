"""
Below is a bare-bones implementation of LinkedList and _Node with the method
insert_after.

Read the docstring for insert_after. Make sure you understand what it's supposed
to do.

Your tasks are listed below.
    1.  In the docstring of insert_after, fill in the expected result.
        This should be a string assigned to the provided variable 'expected'.

    2.  In the docstring of insert_after, fill in the actual result.
        This should be the result of the (currently buggy) implementation of
        insert_after.
        Once again, this should be a string assigned to the provided variable
        'actual'.

    3.  Fix the bug in insert_after.
        You should NOT use any other LinkedList methods -- use only what we've
        provided in quiz5.py

After you finish Task (1) and (3), you should be able to run and pass
the doctests.

Submit your code on MarkUs and run the automated self-test.
Your grade on the quiz will be based solely on the results of the self-test.
(i.e. if you pass all of the tests, you get full marks on the quiz.)
"""
from __future__ import annotations
from typing import Any, Optional


################################################################################
# Below is the implementation of LinkedList.
# Do NOT add any methods to either class, and do NOT modify the __init__
# methods.
#
# You should ONLY modify insert_after.
################################################################################
class LinkedList:
    """A linked list implementation of the List ADT.
    """
    # === Private Attributes ===
    # _first:
    #     The first node in the linked list, or None if the list is empty.
    # _size:
    #     The number of items in this linked list.
    _first: Optional[_Node]
    _size: int

    def __init__(self, items: list) -> None:
        """Initialize a new linked list containing the given items.

        The first node in the linked list contains the first item
        in <items>.
        """
        if items == []:
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
        items = []
        curr = self._first
        while curr is not None:
            items.append(str(curr.item))
            curr = curr.next
        return '[' + ' -> '.join(items) + ']'

    def insert_after(self, marker: Any, item: Any) -> None:
        """Insert <item> after the first time <marker> occurs in this
        linked list.

        Precondition: <marker> is in this linked list.

        >>> lst = LinkedList([1, 3, 2, 6])
        >>> lst.insert_after(3, 4)
        >>> expected = '[1 -> 3 -> 4 -> 2 -> 6]'
        >>> actual = '[1 -> 3 -> 4]'
        >>>
        >>> # If you've done Task 1 and Task 3 correctly, the below should work:
        >>> str(lst) == expected
        True
        """
        curr = self._first
        while curr.item != marker:
            curr = curr.next

        insert = _Node(item)
        next_node = curr.next
        curr.next = insert
        insert.next = next_node


################################################################################
# Below is the implementation of _Node
# Do NOT modify the below in any way. You have no tasks related to _Node.
################################################################################
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


if __name__ == '__main__':
    import doctest
    doctest.testmod()
