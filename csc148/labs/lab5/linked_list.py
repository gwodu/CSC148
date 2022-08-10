"""Lab 5: Linked List Exercises

=== CSC148 Winter 2021 ===
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains the code for a linked list implementation with two classes,
LinkedList and _Node.

All of the code from lecture is here, as well as some exercises to work on.
"""
from __future__ import annotations
from typing import Any, List, Optional


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
    """
    # === Private Attributes ===
    # _first:
    #     The first node in the linked list, or None if the list is empty.
    _first: Optional[_Node]

    def __init__(self, items: list) -> None:
        """Initialize a new linked list containing the given items.

        The first node in the linked list contains the first item
        in <items>.
        """
        if len(items) != 0:
            self._first = _Node(items[0])
            prev_node = self._first
            for num in range(1, len(items)):
                new_node = _Node(items[num])
                prev_node.next = new_node
                prev_node = new_node
        else: self._first = None




    # ------------------------------------------------------------------------
    # Methods from lecture/readings
    # ------------------------------------------------------------------------
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

    def __getitem__(self, index: int) -> Any:
        """Return the item at position <index> in this list.

        Raise IndexError if <index> is >= the length of this list.
        """
        curr = self._first
        curr_index = 0

        while curr is not None and curr_index < index:
            curr = curr.next
            curr_index += 1

        assert curr is None or curr_index == index

        if curr is None:
            raise IndexError
        else:
            return curr.item

    def insert(self, index: int, item: Any) -> None:
        """Insert a the given item at the given index in this list.

        Raise IndexError if index > len(self) or index < 0.
        Note that adding to the end of the list is okay.

        >>> lst = LinkedList([1, 2, 10, 200])
        >>> lst.insert(2, 300)
        >>> str(lst)
        '[1 -> 2 -> 300 -> 10 -> 200]'
        >>> lst.insert(5, -1)
        >>> str(lst)
        '[1 -> 2 -> 300 -> 10 -> 200 -> -1]'
        >>> lst.insert(100, 2)
        Traceback (most recent call last):
        IndexError
        """
        # Create new node containing the item
        new_node = _Node(item)

        if index == 0:
            self._first, new_node.next = new_node, self._first
        else:
            # Iterate to (index-1)-th node.
            curr = self._first
            curr_index = 0
            while curr is not None and curr_index < index - 1:
                curr = curr.next
                curr_index += 1

            if curr is None:
                raise IndexError
            else:
                # Update links to insert new node
                curr.next, new_node.next = new_node, curr.next

    # ------------------------------------------------------------------------
    # Lab Task 1
    # ------------------------------------------------------------------------
    def __len__(self) -> int:
        """Return the number of elements in this list.

        >>> lst = LinkedList([])
        >>> len(lst)              # Equivalent to lst.__len__()
        0
        >>> lst = LinkedList([1, 2, 3])
        >>> len(lst)
        3
        """
        curr = self._first
        count = 0
        while curr is not None:
            count += 1
            curr = curr.next
        return count

    def count(self, item: Any) -> int:
        """Return the number of times <item> occurs in this list.

        Use == to compare items.

        >>> lst = LinkedList([1, 2, 1, 3, 2, 1])
        >>> lst.count(1)
        3
        >>> lst.count(2)
        2
        >>> lst.count(3)
        1
        """
        curr = self._first
        count = 0
        while curr is not None:
            if curr.item == item:
                count += 1
            curr = curr.next
        return count


    def index(self, item: Any) -> int:
        """Return the index of the first occurrence of <item> in this list.

        Raise ValueError if the <item> is not present.

        Use == to compare items.

        >>> lst = LinkedList([1, 2, 1, 3, 2, 1])
        >>> lst.index(1)
        0
        >>> lst.index(3)
        3
        >>> lst.index(148)
        Traceback (most recent call last):
        ValueError
        """
        curr = self._first
        count = 0
        while curr is not None:
            if curr.item == item:
                return count
            else:
                count += 1
                curr = curr.next
        raise ValueError

    def __setitem__(self, index: int, item: Any) -> None:
        """Store item at position <index> in this list.

        Raise IndexError if index >= len(self).

        >>> lst = LinkedList([1, 2, 3])
        >>> len(lst)
        3
        >>> lst[0] = 100  # Equivalent to lst.__setitem__(0, 100)
        >>> lst[1] = 200
        >>> lst[2] = 300
        >>> str(lst)
        '[100 -> 200 -> 300]'
        """
        second_node = self._first.next
        new_node = _Node(item)
        index_count = 0
        node_before = None
        node_after = None
        curr = self._first
        if index == 0:
            self._first = new_node
            new_node.next = second_node
        elif index >= len(self):
            raise IndexError
        else:
            while index_count != index and curr is not None:
                index_count += 1
                node_before = curr
                curr = curr.next
                node_after = curr.next
            #index is either within list_size or at the end of the list
            node_before.next = new_node
            new_node.next = node_after

def swap(lst: LinkedList, i: int, j: int) -> None:
    """Swap the values stored at indexes <i> and <j> in the given linked list.
    Precondition: i and j are >= 0.

    Raise an IndexError if i or j (or both) are too large (out of bounds for this list).
    NOTE: You don't need to create new nodes or change any "next" attributes.
    You can implement this method simply by assigning to the "item" attribute of existing nodes.
    >>> linky = LinkedList([10, 20, 30, 40, 50])
    >>> swap(linky, 0, 3)
    >>> str(linky)
    '[40 -> 20 -> 30 -> 10 -> 50]'
    """
    curr = lst._first
    while curr is not None and j != 0 and i != 0:
        i -= 1
        j -= 1
        curr = curr.next
    if i == 0:
        curr_i = curr
    elif j == 0:
        curr_j = curr

    if i != 0:
        while curr is not None and i != 0:
            i -= 1
            curr = curr.next
        curr_i = curr
    elif j != 0:
        while curr is not None and j != 0:
            j -= 1
            curr = curr.next
        curr_j = curr

    if curr_i is None or curr_j is None:
        raise IndexError

    curr_i.item, curr_j.item = curr_j.item, curr_i.item



if __name__ == '__main__':
    # import python_ta
    # python_ta.check_all()
    import doctest
    doctest.testmod()
