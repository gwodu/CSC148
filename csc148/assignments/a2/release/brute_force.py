"""Assignment 2 - Brute Force Combinations

CSC148, Summer 2021

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

===== Module Description =====

This module constructs all possible file pairs and runs both the bogo
and greedy schedulers, computes the statistics, and writes the statistics
out to multiple csv files. It also optionally plots a statistic of interest
in a boxplot.

You have no tasks associated with this module.  It is provided to you so that
you can compare the performance of the algorithms and notice any patterns or
conclusions you might draw.  You may also find that reviewing the comparison
reveals bugs in your code.
"""

import os
from typing import List, Union, Optional
from a2_command_central import CommandCentral

CAN_PLOT = False

try:
    from matplotlib import pyplot as plt
    CAN_PLOT = True
except ImportError:
    print("matplotlib not found!")

DATA_PATH = "./data"
SF_DATA_PATH = "full_space_fleet"
PASSENGER_DATA_PATH = "full_passenger"
GALAXY_FNAME = "./data/galaxy_data.txt"

SMALL_NUM_FILES = 4


def mean(x: List[Union[int, float]]) -> float:
    """Returns the arithmetic mean of values in <x>.
    """
    return sum(x) / len(x)


def standard_deviation(x: List[Union[int, float]]) -> float:
    """Returns the standard deviation of values in <x>.
    """
    mean_x = mean(x)
    return (sum([(x_i - mean_x) ** 2 for x_i in x])) ** 0.5


def brute(
        fout_individual: str,
        fout_aggregate: str,
        num_files: int = SMALL_NUM_FILES,
        plot_statistic: Optional[str] = None
) -> None:
    """Writes the generated statistics (individual and aggregate) out to
    files determined by <fout_individual> and <fout_aggregate>.

    This function reads from data/full_passenger and data/full_space_fleet
    directories.

    The statistics are generated for every combination of passenger and
    fleet files from file 1 to <num_files>, for both the bogo and greedy
    schedulers.

    For example, if <num_files> is 3, the following combinations
    will be tested with both the bogo and greedy schedulers:

      - fleet file 1, passenger file 1
      - fleet file 1, passenger file 2
      - fleet file 1, passenger file 3
      - fleet file 2, passenger file 1
      - fleet file 2, passenger file 2
      - fleet file 2, passenger file 3
      - fleet file 3, passenger file 1
      - fleet file 3, passenger file 2
      - fleet file 3, passenger file 3

    When <plot_statistic> is not None, a boxplot of the performance according
    to the <plot_statistic> is generated.

    Preconditions:
      - <plot_statistic> is either None, or one of:
        'num_bikes', 'num_empty_bikes', 'average_fill_percent',
        'average_distance_travelled', 'vacant_seats', 'total_fare_collected'
        'deployment_cost', or 'profit'

        As per the keys in the CommandCentral._stats attribute.
      - <num_files> is between 1 and 20, inclusive.

    """
    file_idx = [i for i in range(1, num_files + 1)]
    algorithms = ["bogo", "greedy"]
    passenger_priorities = ["fare_per_dist", "fare_bid", "travel_dist"]

    records = {}
    records["bogo"] = []
    records["greedy"] = {}

    i = 0
    for idx_fleet in file_idx:
        print(f"--- Now running configuration {i} of {num_files ** 2} ---")
        fleet_fname = os.path.join(
            DATA_PATH, SF_DATA_PATH, f"space_fleet_data_{idx_fleet}.txt"
        )
        for idx_passenger in file_idx:
            passenger_fname = os.path.join(
                DATA_PATH, PASSENGER_DATA_PATH, f"passengers_{idx_passenger}.txt"
            )

            # run the experiment on bogo, then on greedy
            for algorithm in algorithms:
                if algorithm == "greedy":
                    for p in passenger_priorities:
                        config = {
                            "scheduler_type": algorithm,
                            "verbosity": 0,
                            "passenger_priority": p,
                            "passenger_fname": passenger_fname,
                            "galaxy_fname": GALAXY_FNAME,
                            "fleet_fname": fleet_fname
                        }
                        cc = CommandCentral(config)
                        stats = cc.run(report=False)
                        all_keys = list(stats.keys())
                        all_keys.sort()

                        if p not in records[algorithm]:
                            records[algorithm][p] = []

                        records[algorithm][p].append([stats[k] for k in all_keys])
                        records["headings"] = all_keys

                else:
                    config = {
                        "scheduler_type": algorithm,
                        "verbosity": 0,
                        "passenger_fname": passenger_fname,
                        "galaxy_fname": GALAXY_FNAME,
                        "fleet_fname": fleet_fname
                    }
                    cc = CommandCentral(config)
                    stats = cc.run(report=False)

                    all_keys = list(stats.keys())
                    all_keys.sort()
                    records[algorithm].append([stats[k] for k in all_keys])
                    records["headings"] = all_keys

        i += num_files

    print(f"Completed all {num_files**2} configurations.")
    f_bogo_individual = open("bogo" + fout_individual, 'w')
    f_bogo_agg = open("bogo" + fout_aggregate, 'w')

    f_greedy_individual = open("greedy" + fout_individual, 'w')
    f_greedy_agg = open("greedy" + fout_aggregate, 'w')

    headings = records["headings"]
    headings_str = ",".join(headings)

    f_bogo_individual.write(headings_str + "\n")
    f_greedy_individual.write(headings_str + "\n")

    f_bogo_agg.write("statistic, mean, standard deviation\n")
    f_greedy_agg.write("statistic, mean, standard deviation\n")

    num_cols = len(records["headings"])
    bogo_data = []
    greedy_data = {}

    for algorithm in records:
        if algorithm == "bogo":
            col = [[] for _ in range(num_cols)]
            for row in records[algorithm]:
                if row != "headings":
                    f_bogo_individual.write(
                        ",".join([str(item) for item in row]) + "\n"
                    )
                for i in range(num_cols):
                    col[i].append(row[i])

                bogo_data = col

            for i in range(num_cols):
                f_bogo_agg.write(f"{headings[i]},"
                                 f"{mean(col[i])},"
                                 f"{standard_deviation(col[i])}\n")

        elif algorithm == "greedy":
            for p in records[algorithm]:
                col = [[] for _ in range(num_cols)]
                f_greedy_individual.write(p + "\n")
                f_greedy_agg.write(p + "\n")

                for row in records[algorithm][p]:
                    f_greedy_individual.write(
                        ",".join([str(item) for item in row]) + "\n"
                    )
                    for i in range(num_cols):
                        col[i].append(row[i])

                    greedy_data[p] = col

                for i in range(num_cols):
                    f_greedy_agg.write(f"{headings[i]},"
                                     f"{mean(col[i])},"
                                     f"{standard_deviation(col[i])}\n")

    fig, ax = plt.subplots()
    if CAN_PLOT and plot_statistic is not None:
        idx = headings.index(plot_statistic.lower())
        ax.set_title(f"{plot_statistic.title()} from Bogo vs. Greedy schedulers for {num_files**2} configurations")
        ax.boxplot(
            [bogo_data[idx]] +
            [greedy_data[p][idx] for p in passenger_priorities]
        )

        label_greedy = ["GreedyScheduler\n" + p for p in passenger_priorities]
        ax.set_xticklabels(["BogoScheduler"] + label_greedy, rotation=0, fontsize=10)
        ax.set_ylabel(f"{plot_statistic.title()}")
        plt.show()


if __name__ == "__main__":
    individual_records_fname = "_individual.csv"
    aggregate_records_fname = "_aggregate.csv"
    n = 20
    brute(
        individual_records_fname,
        aggregate_records_fname,
        num_files=n,
        plot_statistic="profit"
    )

