"""Prep 11 Synthesize: Recursive Sorting Algorithms

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
Copyright (c) 2021 David Liu and Diane Horton

=== Module Description ===
This file includes the recursive sorting algorithms from this week's prep
readings, and two short programming exercises to extend your learning about
these algorithms in different ways.
"""
from typing import Any, List, Tuple


################################################################################
# Mergesort and Quicksort
################################################################################
def mergesort(lst: List) -> List:
    """Return a sorted list with the same elements as <lst>.

    This is a *non-mutating* version of mergesort; it does not mutate the
    input list.

    >>> mergesort([10, 2, 5, -6, 17, 10])
    [-6, 2, 5, 10, 10, 17]
    """
    if len(lst) < 2:
        return lst[:]
    else:
        # Divide the list into two parts, and sort them recursively.
        mid = len(lst) // 2
        left_sorted = mergesort(lst[:mid])
        right_sorted = mergesort(lst[mid:])

        # Merge the two sorted halves. Need a helper here!
        return _merge(left_sorted, right_sorted)


def _merge(lst1: List, lst2: List) -> List:
    """Return a sorted list with the elements in <lst1> and <lst2>.

    Precondition: <lst1> and <lst2> are sorted.
    """
    index1 = 0
    index2 = 0
    merged = []
    while index1 < len(lst1) and index2 < len(lst2):
        if lst1[index1] <= lst2[index2]:
            merged.append(lst1[index1])
            index1 += 1
        else:
            merged.append(lst2[index2])
            index2 += 1

    # Now either index1 == len(lst1) or index2 == len(lst2).

    # The remaining elements of the other list
    # can all be added to the end of <merged>.
    # Note that at most ONE of lst1[index1:] and lst2[index2:]
    # is non-empty, but to keep the code simple, we include both.
    return merged + lst1[index1:] + lst2[index2:]


def quicksort(lst: List) -> List:
    """Return a sorted list with the same elements as <lst>.

    This is a *non-mutating* version of quicksort; it does not mutate the
    input list.

    >>> quicksort([10, 2, 5, -6, 17, 10])
    [-6, 2, 5, 10, 10, 17]
    """
    if len(lst) < 2:
        return lst[:]
    else:
        # Pick pivot to be first element.
        # Could make lots of other choices here (e.g., last, random)
        pivot = lst[0]

        # Partition rest of list into two halves
        smaller, bigger = _partition(lst[1:], pivot)

        # Recurse on each partition
        smaller_sorted = quicksort(smaller)
        bigger_sorted = quicksort(bigger)

        # Return! Notice the simple combining step
        return smaller_sorted + [pivot] + bigger_sorted


def _partition(lst: List, pivot: Any) -> Tuple[List, List]:
    """Return a partition of <lst> with the chosen pivot.

    Return two lists, where the first contains the items in <lst>
    that are <= pivot, and the second is the items in <lst> that are > pivot.
    """
    smaller = []
    bigger = []

    for item in lst:
        if item <= pivot:
            smaller.append(item)
        else:
            bigger.append(item)

    return smaller, bigger


################################################################################
# Synthesize exercises
################################################################################
def mergesort3(lst: List) -> List:
    """Return a sorted version of <lst> using three-way mergesort.

    Three-way mergesort is similar to mergesort, except:
        - it divides the input list into *three* lists of (almost) equal length
        - the main helper merge3 takes in *three* sorted lists, and returns
          a sorted list that contains elements from all of its inputs.

    HINT: depending on your impementation, you might need another base case
    when len(lst) == 2 to avoid an infinite recursion error.

    >>> mergesort3([10, 2, 5, -6, 17, 10])
    [-6, 2, 5, 10, 10, 17]
    """
    # You must NOT use mergesort, sort, or sorted.
    if len(lst) < 2:  # We've provided the base case for you.
        return lst[:]
    else:
        div1 = (len(lst) // 3) + 1
        div2 = 2 * div1
        part1 = lst[: div1]
        part2 = lst[div1: div2]
        part3 = lst[div2:]
        merged1 = mergesort3(part1)
        merged2 = mergesort3(part2)
        merged3 = mergesort3(part3)

        return merge3(merged1, merged2, merged3)


def merge3(lst1: List, lst2: List, lst3: List) -> List:
    """Return a sorted list with the elements in the given input lists.

    Precondition: <lst1>, <lst2>, and <lst3> are all sorted.

    This *must* be implemented using the same approach as _merge; in particular,
    it should use indexes to keep track of where you are in each list.
    This will keep your implementation efficient, which we will be checking for.

    Since this involves some detailed work with indexes, we recommend splitting
    up your code into one or more helpers to divide up (and test!) each part
    separately.
    """

    # Note that we've made it public because we'll be testing it directly.

    # You may call _merge in this function, but you should only call it ONCE
    # at most.
    # i.e. merge the three lists together and use _merge as needed when
    # there's only two lists left to merge.
    index1 = 0
    index2 = 0
    merged_1_2 = []

    while index1 < len(lst1) and index2 < len(lst2):
        if lst1[index1] <= lst2[index2]:
            merged_1_2.append(lst1[index1])
            index1 += 1
        else:
            merged_1_2.append(lst2[index2])
            index2 += 1

    merged_1_2 += lst1[index1:] + lst2[index2:]

    if len(lst3) == 0:
        return merged_1_2

    merged_index = 0
    index3 = 0
    main_merged = []

    while merged_index < len(merged_1_2) and index3 < len(lst3):
        if merged_1_2[merged_index] <= lst3[index3]:
            main_merged.append(merged_1_2[merged_index])
            merged_index += 1
        else:
            main_merged.append(lst3[index3])
            index3 += 1

    return main_merged + merged_1_2[merged_index:] + lst3[index3:]


def kth_smallest(lst: List, k: int) -> Any:
    """Return the <k>-th smallest element in <lst>.

    Raise IndexError if k < 0 or k >= len(lst).
    Note: for convenience, k counts from 0, so kth_smallest(lst, 0) == min(lst).

    Precondition: <lst> does not contain duplicates.

    >>> kth_smallest([10, 20, -4, 3], 0)
    -4
    >>> kth_smallest([10, 20, -4, 3], 2)
    10
    """

    # You may *not* sort the list here (this is easy but not very efficient).
    # Instead, use the following approach, based on quicksort:
    #   1. partition the list based on a chosen pivot:
    #       smaller, bigger = partition(...)
    #   2. Compare len(smaller) against k, and use the result to decide which
    #      list to recurse on (if any). As in your BST prep, you should only
    #      make one recursive call into either <smaller> or <bigger>, not both!
    # if k < 0 or k >= len(lst):
    #     raise IndexError
    # if len(lst) == 0:
    #     return None

    if k < 0 or k > len(lst):
        raise IndexError
    pivot = lst[0]

    smaller, bigger = _partition(lst[1:], pivot)

    # if len(smaller) == 0 :  # not true
    #     return pivot
    if len(smaller) == k:
        return pivot
    else:
        if len(smaller) <= k:
            return kth_smallest(bigger, k - (len(smaller) + 1))
        else:
            return kth_smallest(smaller, k)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={'disable': ['E1136']})
