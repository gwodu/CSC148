"""Testing: a basic example

=== CSC148 Summer 2021 ===
Department of Computer Science,
University of Toronto
Materials replicated from CSC148 Winter 2021
with the permission of Diane Horton.

=== Module description ===
This module contains a simple function to illustrate different
forms of testing we'll use in this course.

If you run this file, you'll run the *doctests* contained in this
file (there's only one, but in general you might have many).
See the accompanying files test_insert.py and test_insert_hypothesis.py
for further test examples.
"""
from typing import List


def insert_after(lst: List[int], n1: int, n2: int) -> None:
    """After each occurrence of <n1> in <lst>, insert <n2>.

    >>> lst = [5, 1, 2, 1, 6]
    >>> insert_after(lst, 1, 99)
    >>> lst
    [5, 1, 99, 2, 1, 99, 6]
    """
    i = 0
    while i < len(lst):
        if lst[i] == n1:
            lst.insert(i + 1, n2)
            if n1 == n2:
                i += 1
        i += 1


if __name__ == '__main__':
    import doctest
    doctest.testmod()
