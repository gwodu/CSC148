from linked_list import _Node, LinkedList

lst = LinkedList([1, 2, 3])
print(len(lst))
len(lst)
lst[0] = 100  # Equivalent to lst.__setitem__(0, 100)
lst[1] = 200
lst[2] = 300
str(lst)
