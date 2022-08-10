"""Testing: a basic example

=== CSC148 Summer 2021 ===
Department of Computer Science,
University of Toronto
Materials replicated from CSC148 Winter 2021
with the permission of Diane Horton.

=== Module description ===
This module contains a few simple unit tests for insert_after.
Note that in order to run this file on your own computer,
you need to have followed our CSC148 Software Guide and installed
all of the Python requirements for the course, including pytest.
"""
from typing import List
from hypothesis import given
from hypothesis.strategies import integers, lists

# Note: you'll need to implement insert_after in a file called
# 'insert.py' for this import to work.
# Check the "Testing" slides for the docstring for insert_after.
from insert import insert_after


@given(lists(integers()), integers(), integers())
def test_returns_none(lst: List[int], n1: int, n2: int) -> None:
    """Test that insert_after always returns None.
    """

    # To be filled in class
    given()


    input_list = [1,2,3,4,5]


    assert 1 == 1

if __name__ == '__main__':
    import pytest
    pytest.main(['test_insert_hypothesis.py'])
