"""CSC148 Lab 4: Abstract Data Types

=== CSC148 Fall 2018 ===
Department of Computer Science,
University of Toronto

=== Module Description ===
In this module, you will write two different functions that operate on a Stack.
Pay attention to whether or not the stack should be modified.
"""
from typing import Any, List


###############################################################################
# Task 1: Practice with stacks
###############################################################################
class Stack:
    """A last-in-first-out (LIFO) stack of items.

    Stores data in a last-in, first-out order. When removing an item from the
    stack, the most recently-added item is the one that is removed.
    """
    # === Private Attributes ===
    # _items:
    #     The items stored in this stack. The end of the list represents
    #     the top of the stack.
    _items: List

    def __init__(self) -> None:
        """Initialize a new empty stack."""
        self._items = []

    def is_empty(self) -> bool:
        """Return whether this stack contains no items.

        >>> s = Stack()
        >>> s.is_empty()
        True
        >>> s.push('hello')
        >>> s.is_empty()
        False
        """
        return self._items == []

    def push(self, item: Any) -> None:
        """Add a new element to the top of this stack."""
        self._items.append(item)

    def pop(self) -> Any:
        """Remove and return the element at the top of this stack.

        Raise an EmptyStackError if this stack is empty.

        >>> s = Stack()
        >>> s.push('hello')
        >>> s.push('goodbye')
        >>> s.pop()
        'goodbye'
        """
        if self.is_empty():
            raise EmptyStackError
        else:
            return self._items.pop()

    def __str__(self):
        rtrn_str = ''
        temp = Stack()
        while not self.is_empty():
            temp.push(self.pop())
        while not temp.is_empty():
            item_ = temp.pop()
            self.push(item_)
            rtrn_str += '->' + '' + str(item_)
        return rtrn_str


class EmptyStackError(Exception):
    """Exception raised when an error occurs."""
    pass


def size(s: Stack) -> int:
    """Return the number of items in s.

    >>> s = Stack()
    >>> size(s)
    0
    >>> s.push('hi')
    >>> s.push('more')
    >>> s.push('stuff')
    >>> size(s)
    3
    """
    side_stack = Stack()
    count = 0
    # Pop everything off <s> and onto <side_stack>, counting as we go.
    while not s.is_empty():
        side_stack.push(s.pop())
        count += 1
    # Now pop everything off <side_stack> and back onto <s>.
    while not side_stack.is_empty():
        s.push(side_stack.pop())
    # <s> is restored to its state at the start of the function call.
    # We consider that it was not mutated.
    return count


def remove_big(s: Stack) -> None:
    """Remove the items in <stack> that are greater than 5.

    Do not change the relative order of the other items.

    >>> s = Stack()
    >>> s.push(1)
    >>> s.push(29)
    >>> s.push(8)
    >>> s.push(4)
    >>> remove_big(s)
    >>> s.pop()
    4
    >>> s.pop()
    1
    >>> s.is_empty()
    True
    """
    holder_stack = Stack()
    while not s.is_empty():
        curr_num = s.pop()
        if curr_num <= 5:
            holder_stack.push(curr_num)
    while not holder_stack.is_empty():
        s.push(holder_stack.pop())



# TODO: implement this function!
def double_stack(s: Stack) -> Stack:
    """Return a new stack that contains two copies of every item in <stack>.

    >>> s = Stack()
    >>> s.push(1)
    >>> s.push(29)
    >>> new_stack = double_stack(s)
    >>> s.pop()  # s should be unchanged.
    29
    >>> s.pop()
    1
    >>> s.is_empty()
    True
    >>> new_items = []
    >>> new_items.append(new_stack.pop())
    >>> new_items.append(new_stack.pop())
    >>> new_items.append(new_stack.pop())
    >>> new_items.append(new_stack.pop())
    >>> sorted(new_items)
    [1, 1, 29, 29]
    """
    pass
    side_stack1 = Stack()
    return_stack = Stack()
    while not s.is_empty():
        num_pop = s.pop()
        side_stack1.push(num_pop)
    while not side_stack1.is_empty():
        num = side_stack1.pop
        s.push(num)
        return_stack.push(num)
        return_stack.push(num)
    return return_stack

def keep_top(stack: Stack) -> None:
    """Remove all items except the top one from the given stack.
    Precondition: <stack> has at least one item.

    >>> s = Stack()
    >>> s.push(10)
    >>> s.push(20)
    >>> s.push(30)
    >>> keep_top(s)
    >>> s.pop()       # TODO: fill in the return value of s.pop() here.
    10
    >>> s.is_empty()
    True"""
    while not stack.is_empty():
        prev_pop = stack.pop()
    stack.push(prev_pop)



if __name__ == '__main__':
    import doctest
    doctest.testmod()
