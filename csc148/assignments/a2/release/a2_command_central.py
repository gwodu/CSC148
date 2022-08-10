"""Assignment 2 - Command Central [Task 5]

CSC148, Summer 2021

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

This module is adapted from the Winter 2021 A1, created by Diane
Horton, Ian Berlott-Attwell, Jonathan Calver, Sophia Huynh, Maryam
Majedi, and Jaisie Sin.

Adapted by: Saima Ali and Marina Tawfik

===== Module Description =====

This module contains class CommandCentral.  It creates the appropriate
scheduler instance according to a configuration dictionary, then
runs the scheduler, generates statistics, and (optionally) reports the
statistics.

This module is responsible for all the reading of data from the data files.
"""

from typing import Dict, List, Union, Optional
from a2_fleet_scheduler import BogoScheduler, GreedyScheduler, FleetScheduler
from a2_space_bikes import SpaceBike, SpaceFleet, Passenger
from a2_distance_map import DistanceMap


def load_fleet_data(fleet_fname: str) -> SpaceFleet:
    """Read SpaceFleet data from <fleet_fname> and return
    an instance of SpaceFleet with all of the SpaceBikes found
    in the <fleet_fname> file.

    Precondition: <fleet_fname> is the path to a file containing fleet data in
                  the form specified in the A2 handout.
    """
    f = open(fleet_fname)

    spacefleet = SpaceFleet()

    line = f.readline()
    while line.strip() != "":
        name = line.strip()
        contents = [item.strip()
                    for item in f.readline().strip().split('\t')]

        id_, max_passengers, fuel_capacity, fuel_usage_rate = \
            contents[0], contents[1], \
            contents[2], contents[3]

        spacebike = SpaceBike(int(id_[3:]), name,
                              int(max_passengers), float(fuel_capacity),
                              float(fuel_usage_rate))
        spacefleet.add_space_bike(spacebike)

        line = f.readline()  # check if this is what's meant to happen
    f.close()

    return spacefleet


def load_galaxy_data(galaxy_fname: str) -> DistanceMap:
    """Read Galaxy data from <galaxy_fname> and return
    an instance of DistanceMap that records the inter-galactic
    distances.

    Precondition: <galaxy_fname> is the path to a file containing galaxy
                  data in the form specified in the A2 handout.
    """

    f = open(galaxy_fname)

    dmap = DistanceMap()

    line = f.readline()
    while line.strip() != "":
        contents = [item.strip() for item in line.split('\t')]
        loc1 = contents[0]
        loc2 = contents[1]

        c1 = float(contents[2])
        c2 = None

        # process the next line
        next_line = f.readline()

        new_contents = [item.strip() for item in next_line.split('\t')]
        # check that second line is not reverse of first
        if len(new_contents) != 3:
            line = next_line
        elif new_contents[0] != loc2 and new_contents[1] != loc1:
            line = next_line
        else:
            c2 = float(new_contents[2])
            line = f.readline()

        dmap.add_distance(loc1, loc2, c1)

        if c2 is not None:
            dmap.add_distance(loc2, loc1, c2)
    f.close()

    return dmap


def load_passenger_data(passenger_fname: str) -> List[Passenger]:
    """Read Passenger data from <passenger_fname> and return
    a List of Passengers.

    Precondition: <passenger_fname> is the path to a file containing
                  passenger data in the form specified in the A2 handout.
    """
    f = open(passenger_fname)

    p_list = []

    line = f.readline()
    while line.strip() != "":
        name = line.strip()

        contents = [item.strip()
                    for item in f.readline().strip().split('\t')]

        bid = float(contents[0].split(":")[-1].strip())
        source = contents[1].split(":")[-1].strip()
        dest = contents[2].split(":")[-1].strip()

        passenger = Passenger(name, bid, source, dest)
        p_list.append(passenger)

        line = f.readline()

    f.close()
    return p_list


class CommandCentral:
    """A command central which runs a particular scheduler with a set of
    configurations, computes the results of the scheduler, and reports
    these results.

    This is achieved through the following steps:

    1. Read in all data from necessary files, and create corresponding objects.
    2. Run a scheduling algorithm to assign passengers to space bikes.
    3. Compute statistics showing how good the assignment of passengers to bikes
    is.
    4. Report the statistics from the scheduler.

    === Public Attributes ===
    verbosity:
      If <verbosity> is non-zero, print step-by-step details regarding the
      scheduling algorithm as it runs.
    scheduler:
      The scheduler to run.
    passengers:
      The passengers to schedule onboard the space bikes.
    fleet:
      The SpaceBikes that passengers are scheduled onboard.
    dmap:
      The distances between locations.

    === Private Attributes ===
    _stats:
      A dictionary of statistics. <_stats>'s value is undefined until
      <self>._compute_stats is called, at which point it contains keys and
      values as described in the A2 handout.
    _unboarded:
      A list of passengers. <_unboarded>'s value is undefined until <self>.run
      is called, at which point it contains the list of passengers that could
      not be scheduled onboard any bikes.

    === Representation Invariants ===
    - <fleet> contains at least one space bike.
    - <dmap> contains all of the distances required to compute the length of
      any possible route for the space bikes in <fleet> for any source and
      destination passengers can request travel between.
    """
    verbosity: int
    passenger_priority: Optional[str]
    passengers: List[Passenger]
    fleet: SpaceFleet
    dmap: DistanceMap
    scheduler: FleetScheduler
    _unboarded: List[Passenger]
    _stats: Dict[str, Union[int, float]]

    def __init__(
            self,
            config: Dict[str, Union[str, int]]
    ) -> None:
        self.verbosity = config['verbosity']

        if "passenger_priority" in config:
            self.passenger_priority = config["passenger_priority"]
        else:
            self.passenger_priority = None
        self.passengers = load_passenger_data(config["passenger_fname"])
        self.fleet = load_fleet_data(config["fleet_fname"])
        self.dmap = load_galaxy_data(config["galaxy_fname"])

        self._stats = {}
        self._unboarded = []

        if config["scheduler_type"] == "bogo":
            self.scheduler = BogoScheduler(self.fleet, self.dmap)
        elif config["scheduler_type"] == "greedy":
            self.scheduler = GreedyScheduler(self.dmap,
                                             config["passenger_priority"])
        #     if self.passenger_priority == "travel_dist":
        #         self.scheduler = GreedyScheduler(self.dmap, _travel_dist)
        #     elif self.passenger_priority == "fare_bid":
        #         self.scheduler = GreedyScheduler(self.dmap, _fare_bid)
        #     elif self.passenger_priority == "fare_per_dist":
        #         self.scheduler = GreedyScheduler(self.dmap, _fare_per_dist)

    def run(self, report: bool = False) -> Dict[str, Union[int, float]]:
        """Run the scheduler and return statistics on the outcome.

        The return value is a dictionary with keys and values are as specified
        in the A2 handout (Task 5).

        If <report> is True, print a report on the statistics from this
        experiment.

        If <self.verbosity> is non-zero, print step-by-step details
        regarding the scheduling algorithm as it runs.
        """

        # This method has been completed for you.
        # DO NOT modify it.

        passengers = self.scheduler.schedule(
            self.passengers, self.fleet.bikes, self.verbosity
        )

        unboarded = passengers[False]
        boarded = passengers[True]

        total_boarded = len(boarded)

        # try to keep scheduling un-boarded passengers
        s = ""
        if report:
            if isinstance(self.scheduler, GreedyScheduler):
                s = "GreedyScheduler"
            else:
                s = "BogoScheduler"
            print(f"---------- Now running {s} -----------")

        i = 0
        while len(boarded) != 0:
            # so as long as passengers continue to be boarded
            if report:
                print(f"ITERATION {i}:\t {total_boarded} "
                      f"BOARDED \t {len(unboarded)} UNBOARDED")
            passengers = self.scheduler.schedule(
                unboarded, self.fleet.bikes, self.verbosity
            )
            unboarded = passengers[False]
            boarded = passengers[True]
            total_boarded += len(boarded)

            i += 1

        self._unboarded = unboarded

        self._compute_stats()
        if report:
            print(f"---- {s} complete in {i} iterations ----")
            print("!!--- Now printing report ---!!")
            self._print_report()
            print("!!--- End of report ---!!")

        return self._stats

    def _compute_stats(self) -> None:
        """Compute the statistics, and store in <self>.stats.
        Keys and values are as specified in the A2 handout under the
        section Task 5.

        Precondition: <self>._run has already been called.
        """

        self._stats = {
            'num_bikes': 0,
            'num_empty_bikes': 0,
            'average_fill_percent': 0,
            'average_distance_travelled': 0,
            'vacant_seats': 0,
            'total_fare_collected': 0,
            'deployment_cost': 0,
            'profit': 0
        }

        self._stats['num_bikes'] = self.fleet.num_space_bikes()
        self._stats['num_empty_bikes'] = self.fleet.num_space_bikes() - \
            self.fleet.num_nonempty_bikes()
        self._stats['average_fill_percent'] = self.fleet.average_fill_percent()
        self._stats['average_distance_travelled'] = \
            self.fleet.average_distance_travelled(self.dmap)
        self._stats['vacant_seats'] = self.fleet.vacant_seats()
        self._stats['total_fare_collected'] = self.fleet.total_fare_collected()
        self._stats['deployment_cost'] = \
            self.fleet.total_deployment_cost(self.dmap)
        self._stats['profit'] = self._stats['total_fare_collected'] - \
            self._stats['deployment_cost']

    def _print_report(self) -> None:
        """Report on the statistics stored in <self>._statistics

        This method is *only* for debugging purposes for your benefit, so
        the content and format of the report is your choice; we
        will not call your run method with <report> set to True.

        Precondition: <self>._compute_stats has already been called.
        """

        return self._stats


if __name__ == "__main__":
    import python_ta
    python_ta.check_all(config={
        'allowed-io': ['load_fleet_data', 'load_galaxy_data',
                       'load_passenger_data', 'run'
                       '_print_report'],
        'allowed-import-modules': ['doctest', 'python_ta', 'typing',
                                   'a2_fleet_scheduler',
                                   'a2_space_bikes',
                                   'a2_distance_map'],
        'disable': ['E1136', 'E9998'],
        'max-attributes': 15,
    })

    # ------------------------------------------------------------------------
    # Change the following config to test your schedulers on different
    # parameters
    # ------------------------------------------------------------------------

    config_base = {
        "scheduler_type": "greedy",
        "verbosity": 0,
        "passenger_priority": "fare_per_dist",
        "passenger_fname": "./data/testing/passengers_off_peak.txt",
        "galaxy_fname": "./data/galaxy_data.txt",
        "fleet_fname": "./data/testing/space_fleet_data_larger.txt"
    }

    cc = CommandCentral(config_base)
    cc.run(report=True)
