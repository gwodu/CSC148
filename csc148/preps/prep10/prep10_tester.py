from prep10 import Tree
def test_doctest():
    t = Tree(1, [])
    t.swap_down()
    # print(t)
    t._subtrees = [Tree(2, []), Tree(3, [])]
    # print(t)
    t.swap_down()
    # print(t)
    t_large = Tree(3, [Tree(5, [Tree(7, [Tree(2, []), Tree(1, [])])]),
                       Tree(4, [])])
    t_large.swap_down()
    assert t_large._subtrees[0]._subtrees[0]._root == 3

def test_personal_test():
    sub4 = Tree(4, [])
    sub10_1 = Tree(10, [Tree(1, []), Tree(2, [])])
    sub10_2 = Tree(10, [Tree(2, []), Tree(1, [])])

    sub3 = Tree(3, [])
    sub1 = Tree(1, [])
    sub5 = Tree(5, [sub4, sub10_1, sub10_2])

    t = Tree(2, [sub3, sub1, sub5])
    print(t)
    t.swap_down()
    assert t._root == 5
    assert t._subtrees[0]._root == 3
    assert t._subtrees[1]._root == 1
    assert t._subtrees[2]._root == 10
    assert t._subtrees[2]._subtrees[0]._root == 4
    assert t._subtrees[2]._subtrees[1]._root == 2
    assert t._subtrees[2]._subtrees[1]._subtrees[0]._root == 1
    assert t._subtrees[2]._subtrees[1]._subtrees[1]._root == 2
    assert t._subtrees[2]._subtrees[2]._root == 10
    assert t._subtrees[2]._subtrees[2]._subtrees[0]._root == 2
    assert t._subtrees[2]._subtrees[2]._subtrees[1]._root == 1


if __name__ == '__main__':
    import pytest
    pytest.main(['prep10_tester.py'])
