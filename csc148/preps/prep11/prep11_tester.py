from prep11 import kth_smallest, _partition, quicksort, merge3, mergesort3
def test_merg3_double_list():
    lst = [7, 2]
    sorted = mergesort3(lst)
    assert sorted == [2, 7]

    lst = [7, 7]
    sorted = mergesort3(lst)
    assert sorted == [7, 7]

    lst = [2, 7]
    sorted = mergesort3(lst)
    assert sorted == [2, 7]

def test_merg3():
    lst = [59, 48, 15, 4, 67, 37, 57, 30, 94, 94, 70, 36, 47, 23, 69, 40, 66, 90, 62, 75, 75, 78, 81, 7, 31, 73, 12, 53, 65, 63, 3]
    sorted = mergesort3(lst)
    assert sorted == [3, 4, 7, 12, 15, 23, 30, 31, 36, 37, 40, 47, 48, 53, 57, 59, 62, 63, 65, 66, 67, 69, 70, 73, 75, 75, 78, 81, 90, 94, 94]

def test_kth():
    lst = [59, 48, 15, 4, 67, 37, 57, 30, 94, 94, 70, 36, 47, 23, 69, 40, 66, 90, 62, 75, 75, 78, 81, 7, 31, 73, 12, 53, 65, 63, 3]
    assert kth_smallest(lst, 0) == 3
    assert kth_smallest(lst, 1) == 4
    assert kth_smallest(lst, 2) == 7
    assert kth_smallest(lst, 3) == 12
    assert kth_smallest(lst, 4) == 15
    assert kth_smallest(lst, 5) == 23
    assert kth_smallest(lst, 6) == 30
    assert kth_smallest(lst, 7) == 31
    assert kth_smallest(lst, 8) == 36
    assert kth_smallest(lst, 9) == 37
    assert kth_smallest(lst, 10) == 40
    assert kth_smallest(lst, 11) == 47
    assert kth_smallest(lst, 12) == 48
    assert kth_smallest(lst, 13) == 53
    assert kth_smallest(lst, 14) == 57
    assert kth_smallest(lst, 15) == 59
    assert kth_smallest(lst, 16) == 62
    assert kth_smallest(lst, 17) == 63
    assert kth_smallest(lst, 18) == 65
    assert kth_smallest(lst, 19) == 66
    assert kth_smallest(lst, 20) == 67
    assert kth_smallest(lst, 21) == 69
    assert kth_smallest(lst, 22) == 70
    assert kth_smallest(lst, 23) == 73
    assert kth_smallest(lst, 24) == 75
    assert kth_smallest(lst, 25) == 75
    assert kth_smallest(lst, 26) == 78
    assert kth_smallest(lst, 27) == 81
    assert kth_smallest(lst, 28) == 90
    assert kth_smallest(lst, 29) == 94
    assert kth_smallest(lst, 30) == 94



if __name__ == "__main__":
    import pytest
    pytest.main(['prep11_tester.py'])
