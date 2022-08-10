"""CSC148 Lab 1

=== CSC148 Summer 2021 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module illustrates a simple unit test for our binary_search function.
"""
from search import binary_search


def test_search() -> None:
    """Simple test for binary_search."""
    assert binary_search([0, 5, 10, 15, 20, 25, 30, 35, 40], 5) == 1

def test_search_empty_list() -> None:
    """Test empty list always return -1"""
    assert binary_search([], 2) == -1

def test_search_last_number() -> None:
    """Test for last integer in list"""
    assert binary_search([0, 5, 10, 15, 20, 25, 30, 35, 40], 40) == 8

def test_search_first_number() -> None:
    """Test for first integer in list"""
    assert binary_search([0, 5, 10, 15, 20, 25, 30, 35, 40], 0) == 0

def test_search_mid_number() -> None:
    """Test for middle integer in list"""
    assert binary_search([0, 5, 10, 15, 20, 25, 30, 35, 40], 20) == 4

if __name__ == '__main__':
    import pytest
    pytest.main(['test_search.py'])
