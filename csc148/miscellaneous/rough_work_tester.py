from miscellaneous.rough_work import sum
from typing import List
from hypothesis import given
from hypothesis.strategies import lists, integers, dictionaries

@given(lists(dictionaries(integers(), integers())))
def test_error_return(lst: List[int]) -> None:
    count = 0
    for num in lst:
        count += num
    assert sum(lst)  == ValueError

if __name__ == '__main__':
    import pytest
    pytest.main(['rough_work_tester.py'])
