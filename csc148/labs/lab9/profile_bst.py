"""Lab 9: Binary Search Trees

=== CSC148 Fall 2019 ===
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains some code for running some timing experiments on
binary search trees.
"""
import random
import sys
from timeit import timeit

from bst import BinarySearchTree

lst = None  # Ignore this. This is to make timeit happy.
SIZES = [100, 200, 400, 800, 1600]


# ------------------------------------------------------------------------
# Task 3
# ------------------------------------------------------------------------
def insert_delete_all(items: list[int]) -> None:
    """Insert the items in <items> into an empty BinarySearchTree, and then
    remove them in the same order they were added.

    Precondition: n >= 0.

    Note: you'll need to first create your own BinarySearchTree here,
    and then call insert and delete on it.
    """
    new_stree = BinarySearchTree(None)
    for i in range(1, 11):
        new_stree.insert(i)
    for i in range(1, 11):
        new_stree.delete(i)


def get_items(size: int, is_sorted: bool) -> list[int]:
    """Return a list of <size> items.

    If is_sorted is True, then the list returned will be in sorted order.
    Otherwise, it's shuffled."""
    items = list(range(size))
    if not is_sorted:
        random.shuffle(items)

    return items


def time_experiment():
    """Run the timing experiment on insert_delete_all for various BST
    sizes and items.

    This function is already completed. You do not have to modify this."""
    global lst  # This is just to make timeit happy. Ignore this.

    # Limit the depth of recursion to a level greater than is needed
    # for this lab exercise.  This will prevent incorrect code that has
    # infinite recursion from crashing Python. We'll discuss this more in
    # lecture.
    sys.setrecursionlimit(2000)

    # For each of a series of list sizes, time insertion and deletion
    # into a bst from a RANDOMLY ORDERED list of that size.
    random_times = []
    for size in SIZES:
        lst = get_items(size, False)
        time = timeit('insert_delete_all(lst)',
                      number=10, globals=globals())
        random_times.append(time)
        print(f'Random list of size {size:>7}, time {round(time, 6)}')

    # For each of a series of list sizes, time insertion and deletion
    # into a bst from a SORTED list of that size.
    sorted_times = []
    for size in SIZES:
        lst = get_items(size, True)
        time = timeit('insert_delete_all(lst)',
                      number=10, globals=globals())
        sorted_times.append(time)
        print(f'Sorted list of size {size:>7}, time {round(time, 6)}')

    return random_times, sorted_times


def plot_experiment():
    """Run the experiment and plot the times in a graph.
    You do not have to change the code below. If you want to understand it,
    please refer to Lab 4 and Lab 5."""
    import matplotlib.pyplot as plt

    # Run the experiments and store the results
    random_time, sorted_times = time_experiment()

    start_plt, = plt.plot(SIZES, random_time, 'ro')
    start_plt.set_label("Random list")

    end_plt, = plt.plot(SIZES, sorted_times, 'bo')
    end_plt.set_label("Sorted list")

    plt.legend()
    plt.xlabel("Size")
    plt.ylabel("Average Time (μs)")

    plt.show()


if __name__ == '__main__':
    plot_experiment()

