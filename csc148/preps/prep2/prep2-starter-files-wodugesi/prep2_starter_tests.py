"""Prep 2 Synthesize Sample Tests

=== CSC148 Summer 2021 ===
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: David Liu, Diane Horton, and Sophia Huynh

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 David Liu, Diane Horton, and Sophia Huynh

=== Module Description ===
This module contains sample tests for Prep 2.
Complete the TODO in this file.
There is also a task inside prep2.py.
Make sure to look at that file and complete the TODO there as well.

We suggest you also add your own tests to practice writing tests and
to be confident your code is correct.

When writing a test case, make sure you create a new function, with its
name starting with "test_". For example:

def test_my_test_case():
    # Your test here

All test cases must have different names (i.e. you cannot have two tests
named test_my_test_case).
"""
from hypothesis import given
from hypothesis.strategies import integers
from prep2 import Spinner, Tweet
from datetime import date


################################################################################
# Part 3
# In this part, you will be fixing a bug within a provided test.
################################################################################
def test_buggy_consecutive_spins() -> None:
    """Test consecutive spins of your Spinner class.
    This test case has a bug in it."""

    # TODO: There is a bug in this test case -- find it and fix it.
    #       In its original state, this test case should NOT pass if
    #       your Spinner is implemented correctly!
    #       Do NOT change or remove any of the lines labelled with
    #       "Do not change this line".

    s = Spinner(6)                          # Do not change this line
    s.spin(2)                               # Do not change this line
    expected_value1 = 2
    assert s.position == expected_value1    # Do not change this line
    s.spin(2)                               # Do not change this line
    expected_value2 = 4
    assert s.position == expected_value2    # Do not change this line


################################################################################
# Sample test cases below
#
# Use the below test cases as an example for writing your own test cases,
# and as a start to testing your prep2.py code.
#
# The self-test on MarkUs runs the tests below, along with a few others.
# Make sure you run the self-test after submitting your code!
#
# WARNING: THIS IS CURRENTLY AN EXTREMELY INCOMPLETE SET OF TESTS!
# We will test your code on a much more thorough set of tests!
################################################################################
def test_doctest() -> None:
    """Test the given doctest in the Spinner class docstring."""
    spinner = Spinner(8)

    spinner.spin(4)
    assert spinner.position == 4

    spinner.spin(2)
    assert spinner.position == 6

    spinner.spin(2)
    assert spinner.position == 0


# This is a hypothesis test; it generates a random integer to use as input,
# so that we don't need to hard-code a specific number of slots in the test.
# For more information on hypothesis (one of the testing libraries we're using),
# please see
# https://www.teach.cs.toronto.edu/~csc148h/winter/notes/testing/hypothesis.html
@given(slots=integers(min_value=1))
def test_new_spinner_position(slots: int) -> None:
    """Test that the position of a new spinner is always 0."""
    spinner = Spinner(slots)
    assert spinner.position == 0


def test_unlike_doctest() -> None:
    """Test the given doctest in the unlike method of Tweet."""
    tweet = Tweet('Sophia', date(2021, 1, 1), 'Happy new year!')
    tweet.like(5)
    assert tweet.likes == 5
    tweet.unlike()
    assert tweet.likes == 4

@given(slots=integers(min_value=1))
def test_randposition(slots: int) -> None:
    """Test spin_randomly method"""
    spin1 = Spinner(slots)
    spin1.spin_randomly()
    assert 0 <= spin1.position < spin1.slots


if __name__ == '__main__':
    import pytest
    pytest.main(['prep2_starter_tests.py'])
