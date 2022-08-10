from typing import List
from mystack import Stack


def puzzle(s: Stack, k: int) -> None:
    s1 = Stack()
    for _ in range(k):
        s1.push(s.pop())
        s2 = Stack()
        while not s.is_empty():
            s2.push(s.pop())
        while not s1.is_empty():
            s.push(s1.pop())
        while not s2.is_empty():
            s.push(s2.pop())

stuff = Stack()
stuff.push('A')
stuff.push('B')
stuff.push('C')
stuff.push('D')
puzzle(stuff, 2)
print(stuff)



