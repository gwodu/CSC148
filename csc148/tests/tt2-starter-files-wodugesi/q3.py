""" CSC148 Summer 2021 Term Test 2

Q3: Linked Lists [25 marks]
-----------------------------------------------------------------------------

This file contains an implementation of the _Node class and a partial
implementation of the LinkedList class discussed during lecture.

    - DO NOT modify the _Node class.
    - DO NOT add any public methods to the LinkedList class.
    - You may add private/special methods to the LinkedList class.

This question has 2 parts:

(i) [5 marks] Add one additional non-redundant docstring example to the
    docstring of the method LinkedList.remove_duplicates.

(ii) [20 marks] Implement the method LinkedList.remove_duplicates according
    to its docstring description.

You may not add any public functions, methods or attributes but you can add
private helper functions/methods. You don't need to provide docstrings or type
annotations for these helpers.

A syntax checker is available to you on MarkUs. It only for syntax error
i.e. it does NOT check for correctness.
"""
from __future__ import annotations
from typing import Optional, Any


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

    def _dupli_check(self, item: Any, index: int) -> bool:
        curr = self._first
        while curr is not None and index > 0:
            if curr.item == item:
                return True
            else:
                curr = curr.next
                index -= 1
        return False

    def remove_duplicates(self) -> None:
        """Remove later duplicate values in this LinkedList, such that each
        item in the linked list appears only once (the first occurence is
        retained).

        You **MUST** modify the LinkedList in place; i.e., you **MUST NOT**
        create any new linked lists or nodes.

        You may not use any other python containers such as
        lists, dictionaries, ....

        >>> my_list = LinkedList(["a", "b", "c",])
        >>> my_list.remove_duplicates()
        >>> print(my_list)
        [a -> b -> c]

        >>> my_list = LinkedList(["a", "a", "b", "c", "a", "a", "b", "a"])
        >>> my_list.remove_duplicates()
        >>> print(my_list)
        [a -> b -> c]
        """
        if self._first is None:
            pass
        else:
            curr = self._first
            index = 1
            while curr.next is not None:
                if self._dupli_check(curr.next.item, index) is True:
                    curr.next = curr.next.next
                    # curr = curr.next
                else:
                    curr = curr.next
                    index += 1


# Not required for term test, but is here to verify the sample solution:
if __name__ == "__main__":
    import python_ta
    python_ta.check_all(config={
        'disable': ['E1136']
    })

    import doctest
    doctest.testmod()
