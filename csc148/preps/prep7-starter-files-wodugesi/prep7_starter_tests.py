"""CSC148 Prep 7:

=== CSC148 Summer 2021 ===
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Sophia Huynh

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 Sophia Huynh

=== Module description ===
Complete the TODO in this file.

When writing a test case, make sure you create a new function, with its
name starting with "test_". For example:

def test_my_test_case():
    # Your test here
"""
from prep7 import contains_non_satisfier


# TODO: Implement test cases such that all of the self-tests on MarkUs pass.
#       You will need to be thorough in your choice of test cases.
#       It may help to consider the test cases that you had to write for prep6.

# While we have provided you a doctest in prep7.py, we will not be
# providing sample test cases this time. The tests you write should help you
# test your own code as well!

def p(n: int) -> bool:
    return n < 10

def test_doctest():
    assert contains_non_satisfier([5, 2, [15, 7], 9], p) == True

def test_single_int_non_satisfier():
    assert contains_non_satisfier(15, p) == True

def test_single_int():
    assert contains_non_satisfier(9, p) == False

def test_single_element_list():
    assert contains_non_satisfier([9], p) == False

def test_empty_list():
    assert contains_non_satisfier([], p) == False

def test_none_wrong():
    assert contains_non_satisfier([1, 2, 3, 4, 5], p) == False

def test_1d_nesting():
    assert contains_non_satisfier([1, 2, 3, 15], p) == True

def test_2d_nesting():
    assert contains_non_satisfier([1, 2, [3, 4, 15], 6, 9], p) == True

def test_3d_nesting():
    assert contains_non_satisfier([1, 2, [3, 4, [15], 8], 1], p) == True

def test_4d_nesting():
    assert contains_non_satisfier([1, 2, [3, 4, [5, 6, [11] ], 8]], p) == True

def test_2d_3d_4dnesting():
    assert contains_non_satisfier([1, 2, 3 ,[5, 6, 7], [1, [1, 1, [20]]]], p) \
           == True

def test_no_mutation():
    test_lst = [1, 2, 3 ,[5, 6, 7], [1, [17]]]
    contains_non_satisfier(test_lst, p)
    assert test_lst == [1, 2, 3 ,[5, 6, 7], [1, [17]]]

def test_first_wrong():
    assert contains_non_satisfier([17, 2, 3 ,[5, 6, 7], [1, [1]]], p) == True

def test_mid_wrong():
    assert contains_non_satisfier([1, 2, 15, 7, 9], p) == True

def test_last_wrong():
    assert contains_non_satisfier([1, 2, 3 ,[5, 6, 7], [1, [1]], 17], p) == True

if __name__ == '__main__':
    import pytest
    pytest.main(['prep7_starter_tests.py'])
