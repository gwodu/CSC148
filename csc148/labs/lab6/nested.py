"""Lab 6: Recursion

=== CSC148 Winter 2021 ===
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains a few nested list functions for you to practice recursion.
"""
from typing import Union, List

def greater_than_all(obj: Union[int, List], n: int) -> bool:
    """Return True iff there is no int in <obj> that is larger than or
    equal to <n> (or, equivalently, <n> is greater than all ints in <obj>).

    >>> greater_than_all(10, 3)
    False
    >>> greater_than_all([1, 2, [1, 2], 4], 10)
    True
    >>> greater_than_all([], 0)
    True
    """
    if isinstance(obj, int):
        return n > obj
    else:
        for sublist in obj:
            if not (sublist, n):
                return False
        return True



def add_n(obj: Union[int, List], n: int) -> Union[int, List]:
    """Return a new nested list where <n> is added to every item in <obj>.

    >>> add_n(10, 3)
    13
    >>> add_n([1, 2, [1, 2], 4], 10)
    [11, 12, [11, 12], 14]
    """
    if isinstance(obj, int):
        return obj + n
    else:
        new_list = []
        for sublist in obj:
            new_list.append(add_n(sublist, n))
        return new_list


def nested_list_equal(obj1: Union[int, List], obj2: Union[int, List]) -> bool:
    """Return whether two nested lists are equal, i.e., have the same value.

    Note: order matters.
    You should only use == in the base case. Do NOT use it to compare
    otherwise (as that defeats the purpose of this exercise)!

    >>> nested_list_equal(17, [1, 2, 3])
    False
    >>> nested_list_equal([1, 2, [1, 2], 4], [1, 2, [1, 2], 4])
    True
    >>> nested_list_equal([1, 2, [1, 2], 4], [4, 2, [2, 1], 3])
    False
    """
    # HINT: You'll need to modify the basic pattern to loop over indexes,
    # so that you can iterate through both obj1 and obj2 in parallel.

    if isinstance(obj1, int) or isinstance(obj2, int):
        return obj1 == obj2
    if len(obj1) != len(obj2):
        return False
    else:
        ...
        for i in range(len(obj1)):
            if not nested_list_equal(obj1[i], obj2[i]):
                return False
            return True



def duplicate(obj: Union[int, List]) -> Union[int, List]:
    """Return a new nested list with all numbers in <obj> duplicated.

    Each integer in <obj> should appear twice *consecutively* in the
    output nested list. The nesting structure is the same as the input,
    only with some new numbers added. See doctest examples for details.

    If <obj> is an int, return a list containing two copies of it.

    >>> duplicate(1)
    [1, 1]
    >>> duplicate([])
    []
    >>> duplicate([1, 2])
    [1, 1, 2, 2]
    >>> duplicate([1, [2, 3]])  # NOT [1, 1, [2, 2, 3, 3], [2, 2, 3, 3]]
    [1, 1, [2, 2, 3, 3]]
    """
    # HINT: in the recursive case, you'll need to distinguish between
    # a <sublist> that is an int and a <sublist> that is a list
    # (put an isinstance check inside the loop).

    if isinstance(obj, int):
        return [obj] * 2
    else:
        new_lst = []
        for sublist in obj:
            if isinstance(sublist, int):
                new_lst.append(sublist)
                new_lst.append(sublist)
            else:
                new_lst.append(duplicate(sublist))
        return new_lst

def all_longer_than(obj: Union[str, List], n: int) -> bool:
    """Return True iff all the strings in <obj> have a length greater than n.
    >>> all_longer_than("a", 3)
    False
    >>> all_longer_than("star", 3)
    True
    >>> all_longer_than([], 2)
    True
    >>> all_longer_than(["some", "body", "once"], 2)
    True
    >>> all_longer_than(["told", ["me", "the", ["world"]], [["is", []], "gonna"]], 2)
    False
    """
    if isinstance(obj, str):
        return len(obj) > n
    else:
        lst = []
        for sublist in obj:
            lst.append(all_longer_than(sublist, n))
            if False in lst:
                return False
    return True

def count_matches(obj: Union[int, List], n: int) -> int:
    """Return the number of times that n occurs in obj.
    >>> count_matches(100, 100)
    1
    >>> count_matches(100, 3)
    0
    >>> count_matches([10, [[20]], [10, [10]]], 10)
    3
    >>> count_matches([10, [[20]], [10, [10]]], 20)
    1
    >>> count_matches([10, [[20]], [10, [10]]], 30)
    0
    """
    if isinstance(obj, int):
        if obj == n:
            return 1
        else:
            return 0
    else:
        count = 0
        for subset in obj:
            count += count_matches(subset, n)
        return count

def all_greater_than(obj: Union[int, List], n: int) -> bool:
    """Return True iff all the items in <obj> are greater than n.
    >>> all_greater_than(13, 10)
    True
    >>> all_greater_than(13, 40)
    False
    >>> all_greater_than([[1, 2, 3], 4, [[5]]], 0)
    True
    >>> all_greater_than([[1, 2, 3], 4, [[5]]], 3)
    False
    >>> all_greater_than([[10, 9, 8], 9, [[5]]], 5)
    False
    """
    if isinstance(obj, int):
        return obj > n
    else:
        for sublist in obj:
            if not all_greater_than(sublist, n):
                return False
    return True

def num_lists(obj: Union[int, List]) -> int:
    """Return the number of list objects in the given nested list.
    If obj is a list itself, include it in the count.
    >>> num_lists(4)
    0
    >>> num_lists([1, 2, 3])
    1
    >>> num_lists([1, [2], [[3, 4]]])  # The four lists are:   [1, [2], [[3, 4]]],   [2],   [[3, 4]],   and   [3, 4].
    4
    """
    if isinstance(obj, int):
        return 0
    else:
        count = 1
        for sublist in obj:
            count += num_lists(sublist)
        return count
ans = num_lists([1, [2], [[3, 4]]])

if __name__ == '__main__':
    ...
    import doctest
    doctest.testmod()

    # import python_ta
    # python_ta.check_all()
