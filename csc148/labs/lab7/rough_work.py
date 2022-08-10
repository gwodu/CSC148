from recursive_list_Ian import RecursiveList


lst1 = RecursiveList([])
selections1 = lst1.selections()
len(selections1)
selections1[0].is_empty()
lst2 = RecursiveList([1, 2, 3, 4])
assert len(lst2.selections()) == 16
for i in range(len(lst2.selections())):
    print(lst2.selections()[i])
# print(lst2.selections()[-1])


def f(x: int) -> int:
    if x == 0:
        return x
    else:
        return f(x - 1)

print(f(100))
