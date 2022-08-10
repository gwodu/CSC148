"""Lab 6: Recursion

=== CSC148 Winter 2021 ===
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains a new *recursive* implementation of the List ADT
called RecursiveList. Study it carefully, and then try implementing the
methods in this class.
"""
from __future__ import annotations
from typing import Any, Callable, Optional, List


class RecursiveList:
    """A recursive implementation of the List ADT.

    Note the structural differences between this implementation and the
    node-based implementation of linked lists from the past few weeks.
    Even though both classes have the same public interface,
    how they implement their methods are quite different!
    """
    # === Private Attributes ===
    # _first:
    #     The first item in the list.
    # _rest:
    #     A list containing the items that come after
    #     the first one.
    _first: Optional[Any]
    _rest: Optional[RecursiveList]

    # === Representation Invariants ===
    # _first is None if and only if _rest is None.
    #     This represents an empty list.

    def __init__(self, items: list) -> None:
        """Initialize a new list containing the given items.

        The first node in the list contains the first item in <items>.
        """
        if items == []:
            self._first = None
            self._rest = None
        else:
            self._first = items[0]
            self._rest = RecursiveList(items[1:])

    def is_empty(self) -> bool:
        """Return whether this list is empty.

        >>> lst1 = RecursiveList([])
        >>> lst1.is_empty()
        True
        >>> lst2 = RecursiveList([1, 2, 3])
        >>> lst2.is_empty()
        False
        """
        return self._first is None

    def __str__(self) -> str:
        """Return a string representation of this list.

        >>> lst = RecursiveList([1, 2, 3])
        >>> str(lst) # Equivalent to lst.__str__()
        '1 -> 2 -> 3'
        """
        if self.is_empty():
            return ''
        elif self._rest.is_empty():
            return str(self._first)
        else:
            return str(self._first) + ' -> ' + str(self._rest)

    def __len__(self) -> int:
        """Return the number of elements in this list.

        >>> lst = RecursiveList([])
        >>> len(lst) # Equivalent to lst.__len__()
        0
        >>> lst = RecursiveList([1, 2, 3])
        >>> len(lst)
        3
        """
        if self.is_empty():
            return 0
        if self._rest.is_empty():
            return 1
        else:
            count = 1
            count += len(self._rest)
            return count

    def __contains__(self, item: Any) -> bool:
        """Return whether <item> is in this list.

        Use == to compare items.

        >>> lst = RecursiveList([1, 2, 3])
        >>> 2 in lst # Equivalent to lst.__contains__(2)
        True
        >>> 4 in lst
        False
        """
        if self.is_empty():
            return False
        elif self._first == item:
            return True
        else:
            return self._rest.__contains__(item)
            # Equivalently, item in self._rest

    def count(self, item: Any) -> int:
        """Return the number of times <item> occurs in this list.

        Use == to compare items.

        >>> lst = RecursiveList([1, 2, 1, 3, 2, 1])
        >>> lst.count(1)
        3
        >>> lst.count(2)
        2
        >>> lst.count(3)
        1
        """
        count = 0
        if self.is_empty():
            return 0
        elif self._first == item:
            count += 1
        count += self._rest.count(item)
        return count

    def __getitem__(self, index: int) -> Any:
        """Return the item at position <index> in this list.

        Precondition: index >= 0.

        Raise IndexError if <index> is >= the length of this list.

        >>> lst = RecursiveList([1, 2, 3])
        >>> lst[0] # Equivalent to lst.__getitem__(0)
        1
        >>> lst[1]
        2
        >>> lst[2]
        3
        >>> lst[3]
        Traceback (most recent call last):
        ...
        IndexError
        """
        # if index >= len(self):  # may be redundant
        #     raise IndexError
        if self.is_empty():
            raise IndexError
        elif index == 0:
            return self._first
        else:
            return self._rest[index - 1]

    ###########################################################################
    # Mutating methods: these methods modify the the list
    ###########################################################################
    def __setitem__(self, index: int, item: Any) -> None:
        """Store item at position <index> in this list.

        Precondition: index >= 0.
        Raise IndexError if index is >= the length of this list.

        >>> lst = RecursiveList([1, 2, 3])
        >>> lst[0] = 100 # Equivalent to lst.__setitem__(0, 100)
        >>> lst[1] = 200
        >>> lst[2] = 300
        >>> lst[3] = 400
        Traceback (most recent call last):
        ...
        IndexError
        >>> str(lst)
        '100 -> 200 -> 300'
        """
        if self.is_empty():
            raise IndexError
        elif index == 0:
            self._first = item
        else:
            self._rest[index - 1] = item

    def pop(self, index: int) -> Any:
        """Remove and return the item at position <index> in this list.

        Precondition: index >= 0.
        Raise IndexError if <index> is >= the length of this list.

        >>> lst = RecursiveList([1, 2, 3])
        >>> lst.pop(2)
        3
        >>> str(lst)
        '1 -> 2'
        >>> lst.pop(1)
        2
        >>> str(lst)
        '1'
        >>> lst.pop(0)
        1
        >>> str(lst)
        ''
        >>> lst.pop(0)
        Traceback (most recent call last):
        ...
        IndexError
        """
        if self.is_empty():
            raise IndexError
        elif index == 0:
            return self._pop_first()
        else:
            return self._rest.pop(index - 1)
        pass

    def insert(self, index: int, item: Any) -> None:
        """Insert the given item in to this list at position <index>.

        Precondition: index >= 0.
        Raise an IndexError if index is > the length of the list.
        Note that it is possible to add to the end of the list
        (when index == len(self)).

        >>> lst = RecursiveList(['c'])
        >>> lst.insert(0, 'a')
        >>> str(lst)
        'a -> c'
        >>> lst.insert(1, 'b')
        >>> str(lst)
        'a -> b -> c'
        >>> lst.insert(3, 'd')
        >>> str(lst)
        'a -> b -> c -> d'
        >>> lst.insert(5, 'd')
        Traceback (most recent call last):
        ...
        IndexError
        """
        if index > len(self):
            raise IndexError
        elif index == 0:
            self._insert_first(item)
        else:
            self._rest.insert(index - 1, item)

    def _pop_first(self) -> Any:
        """Remove and return the first item in this list.

        Raise an IndexError if this list is empty.
        >>> lst = RecursiveList([1, 2, 3, 4, 5, 6])
        >>> lst._pop_first()
        1
        >>> print(lst)
        2 -> 3 -> 4 -> 5 -> 6
        """
        first = self._first
        next_first = self._rest._first
        next_rest = self._rest._rest
        self._first = next_first
        self._rest = next_rest
        return first

    def _insert_first(self, item: Any) -> None:
        """Insert item at the front of this list.

        This should work even if this list is empty.
        >>> lst = RecursiveList([1, 2, 3, 4, 5, 6])
        >>> lst._insert_first(0)
        >>> print(lst)
        0 -> 1 -> 2 -> 3 -> 4 -> 5 -> 6
        """
        first = self._first
        other = self._rest
        new_rec = RecursiveList([])
        new_rec._first = first
        new_rec._rest = other
        self._first = item
        self._rest = new_rec

    ###########################################################################
    # Additional Exercises
    ###########################################################################
    def map(self, f: Callable[[Any], Any]) -> RecursiveList:
        """Return a new recursive list storing the items that are
        obtained by applying f to each item in this recursive list.

        >>> func = str.upper
        >>> func('hi')
        'HI'
        >>> lst = RecursiveList(['Hello', 'Goodbye'])
        >>> str(lst.map(func))
        'HELLO -> GOODBYE'
        >>> str(lst.map(len))
        '5 -> 7'
        """

        if self.is_empty():
            return RecursiveList([])
        else:
            new_lst = RecursiveList([f(self._first)])
            new_lst._rest = self._rest.map(f)
            return new_lst
            # new_lst = [f(self._first)]
            # new_lst.extend(self._rest.map(f))
            # return RecursiveList(new_lst)

    def selections(self) -> List[RecursiveList]:
        """Return a list of all selections from this list.

        You can return the selections in any order.

        >>> lst1 = RecursiveList([])
        >>> selections1 = lst1.selections()
        >>> len(selections1)
        1
        >>> selections1[0].is_empty()
        True
        >>> lst2 = RecursiveList([1, 2, 3])
        >>> len(lst2.selections())
        8
        """
        if self.is_empty():
            return [RecursiveList([])]
        else:
            with_first = []
            rest_selections = self._rest.selections()
            for rec_list in rest_selections:
                # new_rclst = RecursiveList([self._first])
                rec_list_copy = rec_list.copy()
                rec_list_copy._insert_first(self._first)
                with_first.append(rec_list_copy)

        return with_first + rest_selections


    def copy(self) -> RecursiveList:
        """Returns a shallow copy of the RecursiveList
        >>> lst = RecursiveList([1, 2, 3])
        >>> lst_copy = lst.copy()
        >>> print(lst_copy)
        1 -> 2 -> 3
        >>> isinstance(lst_copy, RecursiveList)
        True
        """
        if self.is_empty():
            return RecursiveList([])
        else:
            new_lst = RecursiveList([self._first])
            new_lst._rest = self._rest.copy()
            return new_lst

func = str.upper
func('hi')
lst = RecursiveList(['Hello', 'Goodbye'])
ans = str(lst.map(func))

if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # import python_ta
    # python_ta.check_all()
