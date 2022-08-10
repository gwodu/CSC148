"""
We've defined a recursive function that operates on sub-nested-lists called
semi_homogeneous. Parts of the function have been written for you already.

A nested list is semi-homogeneous if it is a single integer, or if it's a
list satisfying both of these conditions:
    1. Its sub-nested-lists are either all integers or all lists
    2. Its sub-nested-lists are all semi-homogeneous

An empty list is considered to be semi-homogeneous.

Your tasks are listed below.
    1.  In test_single_integer, create a test case that calls
        semi_homogeneous on a single integer.
    2.  In test_list_not_semi_homogeneous, create a test case that calls
        semi_homogeneous on a list that is NOT semi-homogeneous.
    3.  In test_list_with_only_integers, create a test case that calls
        semi_homogeneous on a list that contains only integers.
    4.  In test_list_with_semi_homogeneous_nested_lists, create a test case that
        calls semi_homogeneous on a list with semi-homogeneous nested lists.
    5.  Finish the implementation of semi_homogeneous.

Submit your code on MarkUs and run the automated self-test.
Your grade on the quiz will be based solely on the results of the self-test.
(i.e. if you pass all of the tests, you get full marks on the quiz.)
"""
from typing import Union, List
import pytest


def semi_homogeneous(obj: Union[int, List]) -> bool:
    """Return True if the given nested list is semi-homogeneous.

    A nested list is semi-homogeneous if it is a single integer, or if it's a
    list satisfying both of these conditions:
        1. Its sub-nested-lists are either all integers or all lists
        2. Its sub-nested-lists are all semi-homogeneous

    An empty list is considered to be semi-homogeneous.
    """
    # TODO: Implement this function (Task 5)
    if isinstance(obj, int):
        # TODO: Fill in the base case's return statement
        return True
    else:
        # TODO: Handle the recursive case.
        #       We've started this for you in a particular way:
        #       - sublist_type will be the type that we want all of our sublists
        #         to have. We pick it based on the type of the very first
        #         sublist.
        #       - If we see an element that is not of this type, then we know
        #         obj is not semi-homogeneous.
        #       You may modify this if you wish, but you don't have to.
        sublist_type = None

        for sublist in obj:
            if sublist_type is None:
                sublist_type = type(sublist)
            elif not isinstance(sublist, sublist_type):
                # TODO: Fill in the return statement
                return False

            # TODO: Make a recursive call to semi_homogeneous(sublist) and do
            #       something with the result.
            if not semi_homogeneous(sublist):
                return False
        # TODO: Fill in the return statement
        return True


def test_single_integer() -> None:
    """Test semi_homogeneous on a single integer."""
    # TODO: Fill in the ...s below with an example. (Task 1)
    actual = semi_homogeneous(5)
    expected = True

    assert actual is expected


def test_list_not_semi_homogeneous() -> None:
    """Test semi_homogeneous on a list that is not semi-homogeneous"""
    # TODO: Fill in the ...s below with an example. (Task 2)
    actual = semi_homogeneous([1, "...", 3])
    expected = False

    assert actual is expected


def test_list_with_only_integers() -> None:
    """Test semi_homogeneous on a list with only integers."""
    # TODO: Fill in the ...s below with an example. (Task 3)
    actual = semi_homogeneous([1, 2, 3])
    expected = True

    assert actual is expected


def test_list_with_semi_homogeneous_nested_lists() -> None:
    """Test semi_homogeneous on a list with sub-nested-lists that are all lists
    that are semi-homogeneous."""
    # TODO: Fill in the ...s below with an example. (Task 4)
    actual = semi_homogeneous([[1, 2], [3, 4], [5], [6]])
    expected = True

    assert actual is expected


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    pytest.main(['quiz7.py'])
