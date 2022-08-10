"""CSC148 Prep 4: Abstract Data Types

=== CSC148 Summer 2021 ===
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: David Liu, Diane Horton and Sophia Huynh

All of the files in this directory and all subdirectories are:
Copyright (c) 2020 David Liu, Diane Horton and Sophia Huynh

=== Module description ===
This module contains sample tests for Prep 4. You may use these to test your
code.

Complete the TODO in this file.

When writing a test case, make sure you create a new function, with its
name starting with "test_". For example:

def test_my_test_case():
    # Your test here
"""
from typing import List

from hypothesis import given
from hypothesis.strategies import integers, lists

from lectures.week4.adts import Stack, Queue
from prep4 import peek, reverse_top_two, remove_all, remove_all_but_one, \
     add_in_order


################################################################################
# Part 2
# In prep4.py, we have given you the buggy function add_in_order().
# While the documentation of this function is correct, the implementation is
# not.
#
# Write a test case that will fail this buggy implementation, but pass on a
# working version of add_in_order().
#
# You should run the provided self-test on MarkUs to see whether your test
# correctly meets the requirements.
################################################################################
def test_add_in_order():
    stack = Stack()
    lst = [1,2,3]
    result = []
    add_in_order(stack, lst)
    while not stack.is_empty():
        holder = stack.pop()
        result.append(holder)
    assert result == lst



# Below are provided sample test cases for your use. You are encouraged
# to add additional test cases, but you are not required to do so.
#
# WARNING: THIS IS AN EXTREMELY INCOMPLETE SET OF TESTS!
# You may add your own to practice writing tests and to be confident
# your code is correct.
# For more information on hypothesis (one of the testing libraries we're using),
# please see
# https://www.teach.cs.toronto.edu/~csc148h/winter/notes/testing/hypothesis.html

def test_peek_doctest() -> None:
    """Test the doctest given in peek."""
    stack = Stack()
    stack.push(1)
    stack.push(2)
    assert peek(stack) == 2
    assert stack.pop() == 2


@given(lists(integers(), min_size=1, max_size=100))
def test_peek_general(items: List[int]) -> None:
    """Test that peek works for a large range of stack sizes."""
    stack = Stack()
    for item in items:
        stack.push(item)
    assert peek(stack) == items[-1]
    assert stack.pop() == items[-1]


def test_reverse_top_two_doctest() -> None:
    """Test the doctest given in reverse_top_two."""
    stack = Stack()
    stack.push(1)
    stack.push(2)
    reverse_top_two(stack)
    assert stack.pop() == 1
    assert stack.pop() == 2
    assert stack.is_empty()


def test_remove_all_doctest() -> None:
    """Test the doctest given in remove_all."""
    queue = Queue()
    queue.enqueue(1)
    queue.enqueue(2)
    queue.enqueue(3)
    remove_all(queue)
    assert queue.is_empty()


def test_remove_all_but_one_doctest() -> None:
    """Test the doctest given in remove_all_but_one."""
    queue = Queue()
    queue.enqueue(1)
    queue.enqueue(2)
    queue.enqueue(3)
    remove_all_but_one(queue)
    assert queue.is_empty() is False
    assert queue.dequeue() == 3
    assert queue.is_empty()


if __name__ == '__main__':
    import pytest
    pytest.main(['prep4_starter_tests.py'])
