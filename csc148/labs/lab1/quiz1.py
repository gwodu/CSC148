"""
Below is a set of functions and test cases. In this quiz, you will be
adjusting the test cases, and implementing one of the functions.

Your tasks are listed below.

    1. Read through the function fun1() and fill in the variables in
       test_fun1() as needed.

       You should be filling in either:
       - the variables expected_ages and expected_grades OR
       - the variable expected_error

       These should be filled in with what you would expect to happen if
       we ran the following code:
           ages = (4, 5, 6)
           grades = [10, 11]
           fun1(ages, grades)

    2. Read through the function fun2() and fill in the variables in
       test_fun2() as needed.

       You should be filling in either:
       - the variables expected_letters and expected_age OR
       - the variable expected_error

       These should be filled in with what you would expect to happen if
       we ran the following code:
            letters = ['a', 'b', 'c']
            age = 6
            fun2(letters, age)

    You should be able to run pytest on test_fun1() and test_fun2() to see
    whether you have the correct results.

    3. Implement the function add_on()
       We've provided various options, but only one of them will work properly.
       You should delete all options that don't work.

    You should be able to run doctests on add_on to see if you've chosen
    the right option.

Submit your code on MarkUs and run the automated self-test.
Your grade on the quiz will be based solely on the results of the self-test.
(i.e. if you pass all of the tests, you get full marks on the quiz.)
"""
import pytest
from typing import Any


################################################################################
# Task 1
################################################################################
def fun1(that, other) -> None:
    """A function used in test_fun1. Do not change this."""
    that[1] = 99
    other[1] = 99


def test_fun1() -> None:
    ages = (4, 5, 6)
    grades = [10, 11]

    # TODO: Re-assign the 'expected_' variables as needed (Task 1)
    #       These should be replaced based on what you expect to happen if we
    #       were to run the code:
    #       fun1(ages, grades)

    # If you believe no error is raised, replace the ... with the expected
    # values of ages and grades after running fun1(ages, grades)
    # If you believe an error is raised, don't change this.
    expected_ages = ...
    expected_grades = [10, 99]

    # If you believe an error is raised when running fun1(ages, grades),
    # replace 'AssertionError' with the error type
    # (e.g. TypeError, IndexError, ValueError)
    # If you believe no error is raised, don't change this.
    expected_error = TypeError

    # Do NOT change or remove the code below.
    try:
        fun1(ages, grades)
    except expected_error:
        pass
    else:
        assert ages == expected_ages
        assert grades == expected_grades


################################################################################
# Task 2
################################################################################
def fun2(stuff, junk) -> None:
    """A function used in test_fun2. Do not change this."""
    stuff = stuff + ['hi!']
    junk = junk + 1


def test_fun2() -> None:
    letters = ['a', 'b', 'c']
    age = 6

    # TODO: Re-assign the 'expected_' variables as needed (Task 2)
    #       These should be replaced based on what you expect to happen if we
    #       were to run the code:
    #       fun2(letters, age)

    # If you believe no error is raised, replace the ... with the expected
    # values of letters and age after running fun2(letters, age)
    # If you believe an error is raised, don't change this.
    expected_letters = ['a', 'b', 'c']
    expected_age = 6

    # If you believe an error is raised when running fun2(letters, age),
    # replace 'AssertionError' with the error type
    # (e.g. TypeError, IndexError, ValueError)
    # If you believe no error is raised, don't change this.
    expected_error = AssertionError

    # Do NOT change or remove the code below.
    try:
        fun2(letters, age)
    except expected_error:
        pass
    else:
        assert letters == expected_letters
        assert age == expected_age


################################################################################
# Task 3
################################################################################
def add_on(lst: list[tuple], new: Any) -> None:
    """Add new to the end of each tuple in lst.

    >>> things = [(), (1, 2), (1,)]
    >>> add_on(things, 99)
    >>> things
    [(99,), (1, 2, 99), (1, 99)]
    >>> things = []
    >>> add_on(things, 99)
    >>> things
    []
    >>> things = [(), (), ()]
    >>> add_on(things, 99)
    >>> things
    [(99,), (99,), (99,)]
    """
    # TODO: Implement this function (Task 3)
    #       We have provided a few options for you below. Only one of these
    #       will work correctly, so you may choose accordingly and delete
    #       the options that don't work.
    #       The final result should only have 2 lines (one for the for-loop,
    #       and one for the body of the for-loop.)


    # Option 2: use for i in range(len(lst))
    for i in range(len(lst)):

        # Option 2.3: Reassign lst[i] to lst[i] + (new,)
        lst[i] = lst[i] + (new,)


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    pytest.main(['quiz1.py'])
