""" CSC148 Summer 2021 Term Test 1
Q4: Test Cases and Debugging [20 marks]
-----------------------------------------------------------------

Write pytest test cases that will fail on incorrect implementations
of the function foo(). A sample correct implementation of foo() is
provided.

You are guaranteed that any buggy implementation of foo() will be passed
inputs that obey the type annotations, and return values that obey the
type annotations.

Grading scheme:

    n = # of buggy implementations that fail on your test suite
    N = # of buggy implementations we test using your test suite
    c = 0 if your test suite fails on the _correct_ implementation,
        otherwise 1

    Q4 grade = (n / N) * c

"""

import pytest
from typing import List
from random import randint


def foo(nana: List[int]) -> List[int]:
    """ Modifies the list <nana> such that any elements of
    <nana> that were 7 are a random non-7 integer, and any elements
    of <nana> that were *not* 7 are converted to 7. If there were
    no instances of 7 in <nana>, one 7 is added to the end of <nana>.

    Returns a copy of the original contents of <nana>.
    """
    result = nana.copy()

    has_seven = False
    for i in range(len(nana)):
        if nana[i] == 7:
            nana[i] = randint(8, 100)
            has_seven = True
        else:
            nana[i] = 7

    if not has_seven:
        nana.append(7)

    return result


def test_empty_list():
    nana = []
    result = foo(nana)
    assert result == []
    assert len(nana) == 1
    assert nana == [7]


def test_single_seven():
    nana = [7]
    result = foo(nana)
    assert result == [7]
    assert len(nana) == 1
    assert nana != [7]

def test_no_mutation_with7():
    nana = [ 1, 2, 4, 5, 6, 7]
    foo(nana)
    assert len(nana) == 6
    assert nana[-1] != 7

def test_mutation_no_7():
    nana = [ 1, 2, 4, 5, 6]
    foo(nana)
    assert len(nana) == 6
    assert nana[-1] == 7

def test_mutation_seven_added():
    nana = [ 1, 2, 4, 5, 6]
    foo(nana)
    assert len(nana) == 6
    assert nana[-1] == 7

def test_all_sevens():
    nana = [ 7, 7, 7, 7, 7]
    foo(nana)
    seveness = False
    for i in nana:
        if i == 7:
            seveness = True
            break
    assert seveness == False
    assert len(nana) == 5

def test_all_sevens():
    nana = [ 6, 6, 6, 6, 6]
    foo(nana)
    assert nana == [7, 7, 7, 7, 7, 7]
    assert len(nana) == 6

def test_some_sevens():
    nana = [7, 8, 7, 10, 7]
    foo(nana)
    assert nana[0] != 7
    assert nana[2] != 7
    assert nana[-1] != 7
    assert nana[1] == 7
    assert nana[3] == 7
    assert len(nana) == 5

if __name__ == '__main__':
    pytest.main(['q4.py'])
