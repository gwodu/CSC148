"""CSC148 Lab 4: Abstract Data Types

=== CSC148 Winter 2021 ===
Department of Computer Science,
University of Toronto

=== Module Description ===
This module runs timing experiments to determine how the time taken
to enqueue or dequeue grows for different Queue implementations.
"""
from timeit import timeit
from typing import List, Tuple, Callable
from lab4_adts import Queue, AddToStartQueue, AddToEndQueue

###############################################################################
# Task 3: Running timing experiments
#
# In this part of the lab, you will be conducting timing experiments on Queue
# operations.
#
# We have given you two types of Queues to experiment with:
#    AddToStartQueue:   This Queue uses a list and adds new elements to the
#                       start of the list, removing elements from the end.
#                       i.e. enqueue uses insert(0, item)
#                            dequeue uses pop()
#
#    AddToEndQueue:     This Queue also uses a list, but adds new elements to
#                       the end of the list, removing elements from the front.
#                       i.e. enqueue uses append(item)
#                            dequeue uses pop(0)
###############################################################################
# Experiment Parameters
# Below are our experiment settings: you may want to change these values.
#
# QUEUE_SIZES: This represents the queue sizes we'll be experimenting with.
#              i.e. enqueueing and dequeueing from Queues with size 10000,
#              20000, etc.
# NUM_TRIALS:  This represents the number of times we will repeat an
#              experiment: when we run our timing experiments, we want to get
#              use the average time over a number of trials in order to
#              minimize the effect of any outliers.
###############################################################################
QUEUE_SIZES = [1000, 2000, 4000, 8000, 16000]
NUM_TRIALS = 20


def _setup_queues(qsize: int, n: int, qtype: Callable) -> List[Queue]:
    """Return a list of <n> queues, each with <qsize> elements.
    The returned queues should all be of type qtype.

    qtype is either AddToStartQueue or AddToEndQueue.

    >>> q = _setup_queues(1, 2, AddToStartQueue)
    >>> len(q)
    2
    >>> isinstance(q[0], AddToStartQueue)
    True
    >>> q[0].is_empty()
    False
    >>> _ = q[0].dequeue()
    >>> q[0].is_empty()
    True
    """
    queue_list = []
    for _ in range(n):
        q = qtype()
        for _ in range(qsize):
            q.enqueue(1)
        queue_list.append(q)

    return queue_list


def time_enqueue() -> Tuple[List[float], List[float]]:
    """Run timing experiments for enqueue on both AddToStartQueue and
    AddToEndQueue, returning lists with the average time it took to
    enqueue a single element to queues with sizes QUEUE_SIZES over
    NUM_TRIALS trials."""
    # These two lists will hold our timing results.
    startqueue_times = []
    endqueue_times = []

    # This loop runs the timing experiment for enqueueing one item to
    # AddToStartQueue.
    print("Running AddToStartQueue.enqueue experiments...")
    for queue_size in QUEUE_SIZES:
        # 1. Initialize the sample queues
        queues = _setup_queues(queue_size, NUM_TRIALS, AddToStartQueue)

        # 2. For each queue created, call the function timeit.
        #    timeit takes three arguments:
        #        - a *string* representation of a piece of code to run
        #        - the number of times to run it (just 1 for us)
        #        - globals is a technical argument that you DON'T need to
        #          care about
        time = 0
        for queue in queues:
            time += timeit('queue.enqueue(1)', number=1, globals=locals())

        # 3. Get the average time in microseconds (μs)
        average_time = time / NUM_TRIALS * 1e6

        # 4. Report the average time taken and add that to our list of
        #    results.
        startqueue_times.append(average_time)
        print(f'enqueue: Queue size {queue_size:>7}, time: {average_time}')

    print("Running AddToEndQueue.enqueue experiments...")

    for queue_size in QUEUE_SIZES:
        # 1. Initialize the sample queues
        queues = _setup_queues(queue_size, NUM_TRIALS, AddToEndQueue)

        # 2. For each queue created, call the function timeit.
        #    timeit takes three arguments:
        #        - a *string* representation of a piece of code to run
        #        - the number of times to run it (just 1 for us)
        #        - globals is a technical argument that you DON'T need to
        #          care about
        time = 0
        for queue in queues:
            time += timeit('queue.enqueue(1)', number=1, globals=locals())

        # 3. Get the average time in microseconds (μs)
        average_time = time / NUM_TRIALS * 1e6

        # 4. Report the average time taken and add that to our list of
        #    results.
        endqueue_times.append(average_time)
        print(f'enqueue: Queue size {queue_size:>7}, time: {average_time}')


    # Do not change the return statement below.
    return startqueue_times, endqueue_times


def plot_experiment() -> None:
    """Run the timing experiment on AddToStartQueue and AddToEndQueue
     and plot a graph."""
    import matplotlib.pyplot as plt

    # Run the experiments and store the results
    startqueue_times, endqueue_times = time_enqueue()

    # Plot the results of our experiments and assign labels to each plot.
    # Our call to plt.plot takes 3 arguments:
    #     - The x-coordinates of the values to plot
    #     - The y-coordinates of the values to plot
    #     - The format we want to plot with.
    #       'ro' is 'red circle'
    #       'bo' is 'blue circle'
    #       Other formats include 'rx' (red X), 'bx' (blue X) and many more!
    start_plt, = plt.plot(QUEUE_SIZES, startqueue_times, 'ro')
    start_plt.set_label("AddToStartQueue.enqueue")

    end_plt, = plt.plot(QUEUE_SIZES, endqueue_times, 'bo')
    end_plt.set_label("AddToEndQueue.enqueue")

    # After we finish plotting everything, we can create the legend of
    # our graph and label the axes
    plt.legend()
    plt.xlabel("Queue Size")
    plt.ylabel("Average Time (μs)")

    # Show our plotted results. This line must be called after
    # all of the other setup.
    plt.show()


if __name__ == '__main__':
    time_enqueue()

    # # Uncomment the line below to see the plotted graph once you have
    # # time_enqueue() working.
    plot_experiment()
