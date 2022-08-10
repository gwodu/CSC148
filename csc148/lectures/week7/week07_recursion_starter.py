"""Recursion

=== CSC148 ===
Department of Computer Science,
University of Toronto

=== Module description ===
Starter code for some recursive functions we'll write in Week 07
"""
from typing import List


def binary_search(l: List[int], val) -> int:
    """ Return the index of <val> in <l> if <val> is in <l>,
    and -1 if it is not present.

    Implements binary search to look for <val> in <l>.
    (see Week 1 lab for binary search refresher).

    >>> binary_search([11, 12, 13, 14, 15, 16, 17, 18], 16)
    5
    >>> binary_search([11, 12, 13, 14, 15, 16, 17, 18], 11)
    0
    >>> binary_search([11, 12, 13, 14, 15, 16, 17, 18], 18)
    7
    >>> binary_search([11, 12, 13, 14, 15], 18)
    -1
    >>> binary_search([11, 12, 13, 14, 15], 13)
    2
    >>> binary_search([11, 12, 13, 14, 15], 12)
    1
    """
    mid = len(l) // 2

    add_count = 0

    if mid >= len(l):
        return -1
    elif l[mid] == val:
        return mid
    elif val > l[mid]:
        add_count += mid + 1
        index = binary_search(l[mid + 1:], val)
    else:
        index = binary_search(l[0: mid], val)

    if index == -1:
        return index
    else:
        return index + add_count

class ReturnError(Exception):
    pass

def f(n: int) -> int:
    if n > 5:
        raise ReturnError
    else:
        return 5

def g(n: int) -> int:
    if n > 5:
        f(n)
    else:
        return "Bugs"

s = g(50)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
