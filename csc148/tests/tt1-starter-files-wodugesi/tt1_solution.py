################################################################################
#                                      Q1                                      #
################################################################################

# [25 marks]:
#   5 marks: Address initializer
#   5 marks: Franchise initializer
#   10 marks: recording and processing customers in FIFO order
#   5 marks: Calculating & returning order amount before/after tax

# FastFoodFranchise is functionally identical.


class RetailFranchise:
    def __init__(self, address: Address,
                 name: str, promoted_line: str,
                 catalogue: Dict[str, float]) -> None:
        self.address = address
        self.name = name
        self.promoted_line = promoted_line
        self.catalogue = catalogue
        self.customers = []

    def record_customer(self, customer: Dict[str, int]):
        self.customers.append(customer)

    def checkout(self, tax_rates: Dict[str, float]):
        customer = self.customers.pop(0)
        subtotal = 0
        for k, v in customer.items():
            subtotal += v * self.catalogue[k]
        return subtotal, subtotal * (1 + tax_rates[self.address.province])


class Address:
    def __init__(self, street_number: int, street_name: str,
                 city: str, province: str, postal_code: str,
                 country: str = DEFAULT_COUNTRY) -> None:
        # Do not need to have country as parameter
        self.street_num = street_number
        self.street_name = street_name
        self.city = city
        self.province = province
        self.postal_code = postal_code
        self.country = country
        # alternative
        # self.country = DEFAULT_COUNTRY

################################################################################
#                                      Q2                                      #
################################################################################

# Part A:
# (i) x is None. For versions referring to func_y(), we will adjust the
#   grading scheme to account for the typo.

# (ii) 3 items on the call stack; exact function calls depend on the version

# PART B:
# (i)
# >>> cq = CircularQueue(...)  # a new circular queue
# >>> cq.enqueue(7)
# >>> cq.enqueue(6)
# >>> cq.dequeue()
# 7
# >>> cq.dequeue()
# 6
# >>> cq.enqueue(1)  # a new element is enqueued
# >>> cq.dequeue()
# 7
# >>> cq.dequeue()
# 6
# >>> cq.dequeue()
# 1
# >>> cq.dequeue()
# 7

# (ii)
# The provided implementation of _Node is sufficient. For each node in the
# circular queue, the relationship is defined by when is "next". We do not need
# any additional information about the node.

# (iii)
    class CircularQueue:
        """An implementation of the Circular Queue ADT.

        Follows a  FIFO order of enqueue and dequeue operations,
        where once the last node is dequeued, the position is
        reset to the first node of the queue.

        == Public Attributes ==
        curr
          A reference to the node that has the next priority to
          be dequeued.
        end
          A reference to the node after which the next node would
          be enqueued.
        """
        curr: Optional[_Node]
        end: Optional[_Node]

        def __init__(self) -> None:
            self.curr = None
            self.end = None


# (iv)

# enqueue:              where <node> is the node I am enqueueing, I would
#                       set <node>.next to self.end.next, then set
#                       self.end.next to   <node>.

# dequeue:              I would return self.curr.item, and set self.curr to
#                       self.curr.next.

# search for <item>:    starting at self.curr, I would check whether the
#                       node.item is <item>. If it is, I would return
#                       True. Otherwise, I would keep looping through the
#                       next nodes either until I find the <item> I
#                       am looking for, or I reach self.curr again.

################################################################################
#                                      Q3                                      #
################################################################################

# (a) [5 marks]
#   -1 works for an empty linked list
#   -1 works for a one-item list
#       -0.5 partially works for a one-item list e.g. only if item in list
#   -3 works for multi-item list
#       -1.5 partially works for a multi-item list e.g. only if item in list
#   -0.5 for syntax error (if fixing the error will give them any marks)

# test_general is a sanity check to catch any test cases we might have missed

class LinkedList:
    def __contains__(self, val: Any) -> bool:
        curr = self._first
        while curr is not None:
            if curr.item == val:
                return True
            curr = curr.next
        return False

# (b) [5 marks]: Each running time/explanation is worth 1.25

# i.
#   O(n). LinkedList.intersect inspects/LinkedList.except inspects all
#   n nodes of my_list and calls __contains__ which does a constant
#   amount of time since v is in the first node.
#   Updating the linked list takes a constant amount of time.

# ii.
#   O(m * n). For each node in my_list, you need to compare it to every
#   single node of other_list.


# (c) [5 marks]
#   -2.5 Didn't inherit from Exception
#   -2.5 Didn't define the message (ok if message has typos, incomplete, ...)
#   -0.5 Minor syntax error

# Results from test: test_different_lengths might be helpful

class DifferentLengthError(Exception):
    def __str__(self):
        return "The provided list has a different length from this list"

# (d) [20 marks]
#   -8: correct manipulation:
#       -2: works for a one-item list
#       -3: works for multi-item list
#       -3: works if original list has duplicates
#   -9: lists integrity (assuming it was implemented correctly)
#       -4: modifies the list in place (doesn't create a new list and assigns it
#           to first) and no use of python containers and creates new nodes
#           (this will create cycles anyway)
#       -3: doesn't change repeats
#       -3: adds new nodes after existing nodes
#   -2: raise exception (don't deduct marks if the test fails because of typo)
#   -0.5: syntax error


class LinkedList:
    def repeat_after(self, repeats: LinkedList) -> None:
        curr_node = self._first
        curr_repeats_node = repeats._first
        while curr_node and curr_repeats_node:
            repeats_num = curr_repeats_node.item
            for _ in range(repeats_num):
                new_node = _Node(curr_node.item)
                new_node.next = curr_node.next
                curr_node.next = new_node
                curr_node = new_node
            curr_node = curr_node.next
            curr_repeats_node = curr_repeats_node.next
        if curr_node != curr_repeats_node:
            raise DifferentLengthError

################################################################################
#                                      Q4                                      #
################################################################################

# As indicated on the question
