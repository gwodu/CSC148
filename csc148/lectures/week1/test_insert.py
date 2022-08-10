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
from insert import insert_after

def test_insert_after_at_front() -> None:
    """Test insert_after with one occurrence of n1 at the front of lst.
    """

    # To be filled in class
    assert 1 == 1


if __name__ == '__main__':
    import pytest
    pytest.main(['test_insert.py'])
