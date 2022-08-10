from prep9 import BinarySearchTree

bst = BinarySearchTree(7)
left = BinarySearchTree(3)
left._left = BinarySearchTree(2)
left._right = BinarySearchTree(5)
right = BinarySearchTree(11)
right._left = BinarySearchTree(9)
right._left._left = BinarySearchTree(9)
right._left._right = BinarySearchTree(9)
right._right = BinarySearchTree(13)
bst._left = left
bst._right = right
bst.smaller(6)

assert bst.smaller(13) == [2, 3, 5, 7, 9, 9, 9, 11]
