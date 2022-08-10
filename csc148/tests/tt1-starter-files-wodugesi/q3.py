""" CSC148 Summer 2021 Term Test 1
Q3: Linked Lists [35 marks]
-----------------------------------------------------------------------------

This file contains an implementation of the _Node class and a partial
implementation of the LinkedList class discussed during lecture.

    - DO NOT modify the _Node class.
    - DO NOT add any public methods to the LinkedList class.
    - You may add private/special methods to the LinkedList class.

This question has 4 parts:

(a) [5 marks] Implement the LinkedList special method __contains__ according
to its docstring description.

(b) [5 marks] Consider the provided implementation of LinkedList.difference.
For two LinkedLists, <my_list> of length <n> and <other_list> of length <m>,
indicate the big-oh runtime for my_list.difference(other_list) for cases (i)
and (ii). Briefly justify your answer (you are not required to provide the
exact calculation).

    i.  All nodes in my_list have the same value <v> and the first
        node of other_list has value <v>.

        Big Oh of 1

    ii. All nodes in my_list have different values, none of which appear
        in other_list.

        TODO: Answer here


(c) [5 marks] Create a new user-defined exception, DifferentLengthError,
that has the message:

    "The provided list has a different length from this list"

(d) [20 marks] Implement the method LinkedList.repeat_after according to
its provided docstring.

"""
from __future__ import annotations

from typing import Any, Optional


class DifferentLengthError(Exception):

    def __str__(self):
        return "The provided list has a different length from this list"

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

    def __contains__(self, val: Any) -> bool:           #O(len(self) - index of val)
        """Return True if this LinkedList includes <val>, and False
        otherwise.

        This is a special method that is called when you use the in operator.

        >>> bucket_list = LinkedList([
        ...     "Paris", "Toronto", "New Orleans", "London", "Cairo"
        ... ])
        >>> "New Orleans" in bucket_list
        True
        >>> "Tokyo" in bucket_list
        False
        """
        curr = self._first
        while curr is not None:
            if curr.item == val:
                return True
            else:
                curr = curr.next

    def difference(self, other: LinkedList) -> None:
        """Modify this LinkedList by removing all nodes <n> where <n>.item
        appears in <other>.

        >>> my_list = LinkedList([
        ...     "a", "a", "b", "c", "a", "a", "b", "c"
        ... ])
        >>> my_list.difference(LinkedList(["a", "b"]))
        >>> print(my_list)
        [c -> c]
        """

        # This method is provided for you. Do NOT change it.

        prev_node, curr_node = None, self._first  #1

        while curr_node:

            if curr_node.item in other:
                if prev_node:
                    prev_node.next = curr_node.next
                else:
                    self._first = curr_node.next
            else:
                prev_node = curr_node

            curr_node = curr_node.next

    def repeat_after(self, repeats: LinkedList) -> None:
        """Modify this LinkedList by repeating each node the number of times
        specified in <repeats>.

        Each node <r> at position <i> in <repeats> specifies the number of
        **new** nodes to be added **after** the corresponding node <n> at
        position <i> in this LinkedList. The new nodes added after <n> have
        the same item as <n>.item. The original nodes of the LinkedList must
        not be modified.

        Raise DifferentLengthError if <repeats> doesn't have the same number
        of elements as this LinkedList (it's OK if you have already modified
        the LinkedList at this point).

        Do **NOT** use any Python lists, dictionaries, sets, tuples, ... to
        implement this method.

        Precondition:
          - Each node <r> in <repeats> has <r>.item >= 0

        >>> my_list = LinkedList(['a', 'b', 'c', 'd'])
        >>> original_first_id = id(my_list._first)
        >>> repeats_num = LinkedList([1, 0, 2, 1])
        >>> my_list.repeat_after(repeats_num)
        >>> print(my_list)
        [a -> a -> b -> c -> c -> c -> d -> d]
        >>> original_first_id == id(my_list._first)
        True
        >>> id(my_list._first) == id(my_list._first.next)
        False
        """

        # TODO: Implement this method according to its docstring

        # TODO: Don't forget to raise DifferentLengthError if <repeats> is
        #   not the same length as this LinkedList (it's OK if you have
        #   already modified the LinkedList at this point)

        curr_self = self._first
        curr_repeats = repeats._first

        while curr_repeats is not None:
            if curr_self is None:
                raise DifferentLengthError
            next = curr_self.next
            for i in range(curr_repeats.item):
                new_node = _Node(curr_self.item)
                curr_self.next = new_node
                curr_self = new_node    #curr_self is most recent node
            curr_self.next = next
            curr_self = next #curr_self is now next item
            curr_repeats = curr_repeats.next
        if curr_self is not None:
            raise DifferentLengthError



# Not required for term test, but is here to verify the sample solution:
if __name__ == "__main__":
    import python_ta
    python_ta.check_all(config={
        'disable': ['E1136']
    })

    import doctest
    doctest.testmod()
