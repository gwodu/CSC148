"""Prep 6 Synthesize

=== CSC148 Summer 2021 ===
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: David Liu and Diane Horton

All of the files in this directory and all subdirectories are:
Copyright (c) 2020 David Liu and Diane Horton

=== Module Description ===
Your task in this prep is to implement each of the following recursive functions
on nested lists, using the following steps for *Recursive Function Design*:

1.  Identify the recursive structure of the input (in this case, always a nested
    list), and write down the code template for nested lists:

    def f(obj: Union[int, List]) -> ...:
        if isinstance(obj, int):
            ...
        else:
            ...
            for sublist in obj:
                ... f(sublist) ...
            ...

2.  Implement the base case(s) directly (in this case, a single integer).
3.  Write down a concrete example with a somewhat complex argument, (in this
    case, a nested list with around 3 sub-nested-lists), and then write down
    the relevant recursive calls and what they should return.
4.  Determine how to combine the recursive calls to compute the correct output.
    Make sure you can express this in English first, and then implement your
    idea.

HINT: The implementations here should be similar to ones you've seen
before in the readings or comprehension questions.
"""
from typing import Union, List


def num_positives(obj: Union[int, List]) -> int:
    """Return the number of positive integers in <obj>.

    Remember, 0 is *not* positive.

    >>> num_positives(17)
    1
    >>> num_positives(-10)
    0
    >>> num_positives([1, -2, [-10, 2, [3], 4, -5], 4])
    5
    """
    if isinstance(obj, int):
        if obj > 0:
            return 1
        else:
            return 0
    else:
        pos_count = 0
        for sublist in obj:
            pos_count += num_positives(sublist)
        return pos_count
    return 0


def nested_max(obj: Union[int, List]) -> int:
    """Return the maximum integer stored in nested list <obj>.

    Return 0 if <obj> does not contain any integers.

    Precondition: all integers in <obj> are > 0.

    >>> nested_max(17)
    17
    >>> nested_max([1, 2, [1, 2, [3], 4, 5], 4])
    5
    """
    if isinstance(obj, int):
        return obj
    else:
        if len(obj) == 0:
            return 0
        num_lst = []
        for sublist in obj:
            num_lst.append(nested_max(sublist))
    return max(num_lst)


def max_length(obj: Union[int, List]) -> int:
    """Return the maximum length of any list in nested list <obj>.

    The *maximum length* of a nested list is defined as:
    1. 0, if <obj> is a number.
    2. The maximum of len(obj) and the lengths of the nested lists contained
       in <obj>, if <obj> is a list.

     >>> max_length(17)
     0
     >>> max_length([1, 2, [1, 2], 4])
     4
    >>> max_length([1, 2, [1, 2, [3, 4, 5, [6, 7 ,8 ,9, 10, 11, 12, 13, 14], 7, 8, 9], 4, 5], 4])
    9
    """
    # lst_lst = []
    # lst_len = []
    # if isinstance(obj, int):
    #     return 0
    # else:
    #     lst_len = []
    #     lst_len.append(len(obj))
    #     for sublist in obj:
    #         if isinstance(sublist, list):
    #             lst_len.append(len(sublist))
    #             lst_len.append(max_length(sublist))
    #     dogs = lst_len
    #     return dogs
    #     return nested_max(lst_len)

    if isinstance(obj, int):
        return 0
    else:
        max_s = len(obj)
        for sublist in obj:
            curr = max_length(sublist)
            if max_s < curr:
                max_s = curr
        return max_s


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={'disable': ['E1136']})

# for sublist in obj:
#     lst = []
#     lst.append(max_length(sublist))
#     lst_lst.append(lst)
#
# lst_len = []
# for lst_ in lst_lst:
#     lst_len.append(len(lst_))
# return lst_len
