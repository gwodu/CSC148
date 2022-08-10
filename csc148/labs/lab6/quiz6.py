"""
Below is an implementation of the recursive function count_odd which operates
on a nested list. This implementation has a bug which you'll fix in Task 3.

Your tasks are listed below.
    1.  Identify the three recursive calls that are made when we call
        count_odd([1, [2, 6, 5], [9, [8, 7]]])

        In the doctest of count_odd, replace the ...s with the recursive
        calls that are made, along with what we expect this to return.

    2.  In the doctest of count_odd, fill in the expected result of the call
        count_odd([1, [2, 6, 5], [9, [8, 7]]])

    3.  Currently, count_odd has a bug in it. Find the bug and fix it.

Submit your code on MarkUs and run the automated self-test.
Your grade on the quiz will be based solely on the results of the self-test.
(i.e. if you pass all of the tests, you get full marks on the quiz.)
"""
from typing import Union, List


def count_odd(obj: Union[int, List]) -> int:
    """Return the number of odd numbers in <obj>.

    TODO: Task 1
          Consider the call count_odd([1, [2, 6, 5], [9, [8, 7]]])
          In the doctest below, fill in the "..." with the three recursive
          calls that are made in count_odd([1, [2, 6, 5], [9, [8, 7]]])
          and what each call *should* return.

          e.g. if the first recursive call was made to the value 15, then
               you would replace the ... to have
               call_1 = 15

    >>> call_1 = 1                # TODO: Fill in the ...
    >>> actual_1 = count_odd(call_1)
    >>> expected_1 = 1            # TODO: Fill in the ...
    >>> expected_1 == actual_1
    True
    >>> call_2 = [2, 6, 5]                # TODO: Fill in the ...
    >>> actual_2 = count_odd(call_2)
    >>> expected_2 = 1            # TODO: Fill in the ...
    >>> expected_2 == actual_2
    True
    >>> call_3 = [9, [8, 7]]                # TODO: Fill in the ...
    >>> actual_3 = count_odd(call_3)
    >>> expected_3 = 2            # TODO: Fill in the ...
    >>> expected_3 == actual_3
    True
    >>> # TODO: Fill in the expected value below. (Task 2)
    >>> actual = count_odd([1, [2, 6, 5], [9, [8, 7]]])
    >>> expected = 4              # TODO: Fill in the ...
    >>> actual == expected
    True
    """
    if isinstance(obj, int):
        if obj % 2 == 0:
            return 0
        else:
            return 1
    else:
        odd_count = 0
        for sublist in obj:
            odd_count += count_odd(sublist)
        return odd_count

if __name__ == '__main__':
    import doctest
    doctest.testmod()
