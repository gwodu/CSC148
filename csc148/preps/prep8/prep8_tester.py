from preps.prep8.prep8 import Tree

def test_num_negatives():
    t3 = Tree(-11, [Tree(-2, [Tree(-1, [Tree(-20, []) ]) ]), Tree(10, []), Tree(-30, [])])
    assert t3.num_negatives() == 5

def test_maximum():
    t3 = Tree(-11, [Tree(-2, [Tree(-1, [Tree(-20, []) ]) ]), Tree(10, []), Tree(30, [])])
    assert t3.maximum() == 30

def test_height():
    t3 = Tree(-11, [Tree(-2, [Tree(-1, [Tree(-20, []) ]) ]), Tree(10, [Tree(2, [Tree(5, [])])]), Tree(-30, [])])
    assert t3.height() == 4

def test_contains():
    t3 = Tree(-11, [Tree(-2, [Tree(-1, [Tree(-20, []) ]) ]), Tree(10, []), Tree(-30, [])])
    assert -11 in t3
    assert 2000 not in t3
    assert -20 in t3
    assert -30 in t3


if __name__ == "__main__":
    import pytest
    pytest.main(['prep8_tester.py'])
