from typing import Union, List
from preps import prep6

# def first_at_depth(obj: Union[int, List], d: int) -> Optional[int]:
#     """Return the first (leftmost) item in <obj> at depth <d>.
#
#     Return None if there is no item at depth <d>.
#
#     Precondition: d >= 0.
#
#     ===Sample Usage===
#     >>> first_at_depth(9, 0)
#     9
#     >>> first_at_depth([1, 2], 0)
#     None
#     >>> first_at_depth([1], 1)
#     1
#     >>> first_at_depth([1, [2, 3, 4], 2], 2)
#     2
#     >>> first_at_depth([1, [2, 3, [4], 5] 6], 3)
#     4
#     >>> first_at_depth([1, [2], [[3]]], 3)
#     3
#     """
#     if d == 0 and not isinstance(obj, int):
#         return None
#     if isinstance(obj, int):
#         return obj
#     if d == 1:
#         return obj[0]
#     else:
#         sub_count = 1
#         for sublist in obj:
#             sublist += 1

i = [1,2,3]
for item in i:
    rmve = i.pop()
    i.append(rmve)

print(i)
