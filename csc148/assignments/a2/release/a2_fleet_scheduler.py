"""Assignment 2 - Scheduling Passengers [Task 4]

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

This module contains the abstract FleetScheduler class, as well as the two
subclasses BogoScheduler and GreedyScheduler, which implement the two
scheduling algorithms described in the handout.
"""

import random
from typing import List, Dict, Callable, Any, Optional, Union

from a2_space_bikes import Passenger, SpaceBike, SpaceFleet
from a2_container import PriorityQueue
from a2_distance_map import DistanceMap


class FleetScheduler:
    """A fleet scheduler that decides which passengers will board which space
    bikes, and what route each space bike will take.

    This is an abstract class.  Only child classes should be instantiated.
    """

    def schedule(
            self, passengers: List[Passenger],
            space_bikes: List[SpaceBike],
            verbosity: int = 0
    ) -> Dict[bool, List[Passenger]]:
        """Schedule a list of passengers, <passengers> to board
        the SpaceBikes in <space_bikes>.

        Mutate the SpaceBike objects in <space_bikes> to reflect
        the passengers that have boarded and to update the route
        they will take.

        Return a mapping of bool to a List of passengers, where
        True maps to boarded passengers and False maps to unboarded
        passengers.

        If <verbosity> is greater than zero, print step-by-step details
        regarding the scheduling algorithm as it runs.  This is *only*
        for debugging purposes for your benefit, so the content and
        format of this information is your choice; we will only test your
        code with <verbosity> set zero.
        """
        raise NotImplementedError


class BogoScheduler(FleetScheduler):
    """A BogoScheduler
    ===Private Attributes===
    _space_fleet: an instance of class SpaceFleet
    _distance_map: an instance of class DistanceMap
    """

    _space_fleet: SpaceFleet
    _distance_map: DistanceMap

    def __init__(self, space_fleet: SpaceFleet, distance_map: DistanceMap) ->\
            None:
        """Initialise an instance of BogoScheduler"""
        self._space_fleet = space_fleet
        self._distance_map = distance_map

    def schedule(
            self, passengers: List[Passenger],
            space_bikes: List[SpaceBike],
            verbosity: int = 0
    ) -> Dict[bool, List[Passenger]]:
        """Randomly schedule <passengers> to board space bikes from
        <space_bikes> and return a Dictionary where True and False are the keys,
        and they map to the passengers that where able to board, and those that
        weren't
        >>> sf = SpaceFleet()
        >>> b1 = SpaceBike(100, "Nova Bike", 20, 1, 0.5)
        >>> b2 = SpaceBike(100, "Nova Bike", 20, 50.0, 0.5)

        >>> sf.add_space_bike(b1)
        >>> sf.add_space_bike(b2)

        >>> dmap = DistanceMap()
        >>> dmap.add_distance("Earth", "Mars", 0.3)
        >>> dmap.add_distance("Earth", "Venus", 10)
        >>> dmap.add_distance("Earth", "Jupiter", 0.2)
        >>> dmap.add_distance("Mars", "Venus", 0.5)
        >>> dmap.add_distance("Mars", "Jupiter", 0.5)
        >>> dmap.add_distance("Mars", "Earth", 50)

        >>> p0 = Passenger("Jeffery", 1.0, "Earth", "Mars")
        >>> p1 = Passenger("MaryAnn Jacobs", 1.0, "Earth", "Mars")
        >>> p2 = Passenger("Jefferson Pak", 1.0, "Earth", "Venus")
        >>> p3 = Passenger("Gabriel Aderantin", 1.0, "Earth", "Mars")
        >>> p4 = Passenger("Michelle Spatswick", 1.0, "Earth", "Venus")
        >>> p5 = Passenger("Wuami Yause", 1.0, "Earth", "Mars")
        >>> p6 = Passenger("Independence John", 1.0, "Juniper", "Harper")

        >>> passengers = [p0, p1, p2, p3, p4, p5, p6]

        >>> bs = BogoScheduler(sf, dmap)
        >>> bike_list = sf.bikes
        >>> board_dict = bs.schedule(passengers, bike_list,\
        verbosity= 10)
        >>> b1.is_empty()
        False
        >>> b2.is_empty()
        False
        >>> b1.num_passengers() + b2.num_passengers() == len(board_dict[True])
        True
        >>> len(board_dict[False]) == 1
        True
        >>> len(board_dict[False]) + len(board_dict[True])
        7
        """
        board_dict = {True: [], False: []}  # dictionary to be returned
        # shallow copy of passengers to prevent mutation
        passenger_list = passengers.copy()
        # loop through for as many passengers there are
        for _ in range(len(passengers)):
            chosen_passenger = random.choice(passenger_list)
            passenger_list.remove(chosen_passenger)

            # loop through space_bikes until end of list or chosen_passenger
            # is chosen
            b = 0
            while b < len(space_bikes) and \
                    not space_bikes[b].board(chosen_passenger,
                                             self._distance_map):
                b += 1
            if b < len(space_bikes):  # chosen_passenger was boarded
                board_dict[True].append(chosen_passenger)
            else:  # chosen_passenger was not boarded
                board_dict[False].append(chosen_passenger)
        return board_dict


class GreedyScheduler(FleetScheduler):
    """A GreedyScheduler
    ===Attributes===
    _distance_map: an instance of class DistanceMap
    _passenger_priority: the priority on which a passenger will be chosen
    _passenger_priority_str: the passenger priority
    """
    _distance_map: DistanceMap
    _passenger_priority_str: str
    _passenger_priority: Callable[[Any, Any], bool]

    def __init__(self, _distance_map: DistanceMap,
                 _passenger_priority_str: str) -> None:
        """Initialise an instance of GreedyScheduler
        >>> dmap = DistanceMap()
        >>> dmap.add_distance("Earth", "Mars", 1.0)
        >>> dmap.add_distance("Mars", "Jupiter", 1.0)
        >>> dmap.add_distance("Jupiter", "Fr18", 1.0)
        >>> p1 = Passenger("James Cameron", 1.0, "Earth", "Mars")
        >>> p2 = Passenger("James Cameron,", 2.0, "Mars", "Jupiter")
        >>> p3 = Passenger("James Cameron,,", 1.0, "Fr18", "Jupiter")
        >>> b1 = SpaceBike(10000, 'Nova Bike', 20, 8.0, 0.5)
        >>> b2 = SpaceBike(10001, 'Nova Bike', 20, 8.0, 0.5)
        >>> b3 = SpaceBike(10002, 'Nova Bike', 20, 8.0, 0.5)
        >>> space_bikes = [b1, b2, b3]
        >>> passegers = [p1, p2, p3]
        >>> gs = GreedyScheduler(dmap, "fare_per_dist")
        >>> gs._distance_map == dmap
        True

        """
        self._distance_map = _distance_map
        self._passenger_priority_str = _passenger_priority_str
        if self._passenger_priority_str == "fare_bid":
            self._passenger_priority = _fare_bid
        elif self._passenger_priority_str == "fare_per_dist":
            self._passenger_priority = _fare_per_dist
        elif self._passenger_priority_str == "travel_dist":
            self._passenger_priority = _travel_dist

    def _load_queue(self, passenger_list: List[Passenger]) -> PriorityQueue:
        """Return a PriorityQueue instance with passengers as items
        >>> dmap = DistanceMap()
        >>> dmap.add_distance("Earth", "Mars", 1.0)
        >>> dmap.add_distance("Mars", "Jupiter", 1.0)
        >>> dmap.add_distance("Jupiter", "Fr18", 1.0)
        >>> p1 = Passenger("James Cameron", 1.0, "Earth", "Mars")
        >>> p2 = Passenger("James Cameron,", 2.0, "Mars", "Jupiter")
        >>> p3 = Passenger("James Cameron,,", 1.0, "Fr18", "Jupiter")
        >>> b1 = SpaceBike(10000, 'Nova Bike', 20, 8.0, 0.5)
        >>> b2 = SpaceBike(10001, 'Nova Bike', 20, 8.0, 0.5)
        >>> b3 = SpaceBike(10002, 'Nova Bike', 20, 8.0, 0.5)
        >>> space_bikes = [b1, b2, b3]
        >>> passengers = [p1, p2, p3]
        >>> gs = GreedyScheduler(dmap, "fare_per_dist")
        >>> gs._distance_map == dmap
        True
        >>> pqueue = gs._load_queue(passengers)
        >>> pqueue._first.val == p2
        True
        >>> pqueue._first.next.val == p1
        True
        >>> pqueue._first.next.next.val == p3
        True
        """
        passenger_queue = PriorityQueue(self._passenger_priority)
        for passenger in passenger_list:
            passenger.give_distance(self._distance_map)  # update passenger dist
            passenger_queue.add(passenger)
        return passenger_queue

    def schedule(
            self, passengers: List[Passenger],
            space_bikes: List[SpaceBike],
            verbosity: int = 0
    ) -> Dict[bool, List[Passenger]]:
        """Try and board every passenger on a space bike according to the
        instructions in the handouts
        """
        board_dict = {True: [], False: []}  # dictionary to be returned
        pqueue = self._load_queue(passengers)
        while not pqueue.is_empty():
            curr_passenger = pqueue.remove()
            bike_choice = _space_bike_priority(curr_passenger,  # pick bike
                                               space_bikes,
                                               self._distance_map)
            if bike_choice is None:
                board_dict[False].append(curr_passenger)
            else:
                if bike_choice.board(curr_passenger, self._distance_map):
                    board_dict[True].append(curr_passenger)
                else:
                    board_dict[False].append(curr_passenger)

        return board_dict


def _travel_dist(passenger_1: Passenger, passenger_2: Passenger) -> bool:
    """Return True iff passenger_1.distance is less than passenger_2.distance,
    otherwise, return False

    >>> dmap = DistanceMap()
    >>> dmap.add_distance("Earth", "Venus", 1.3)
    >>> dmap.add_distance("Venus", "Glieise", 1.0)
    >>> dmap.add_distance("Glieise", "JFr14", 0.751)
    >>> p1 = Passenger("James Cameron", 1.0, "Earth", "Venus")
    >>> p1.give_distance(dmap)
    >>> p2 = Passenger("Catwell Romanuel", 1.0, "Glieise", "JFr14")
    >>> p2.give_distance(dmap)
    >>> _travel_dist(p1, p2)
    False
    >>> _travel_dist(p2, p1)
    True
    """
    return passenger_1.distance < passenger_2.distance


def _fare_bid(passenger_1: Passenger, passenger_2: Passenger) -> bool:
    """Return True iff passenger_1 has a higher bid than passenger_2
    >>> dmap = DistanceMap()
    >>> dmap.add_distance("Earth", "Venus", 1.3)
    >>> dmap.add_distance("Venus", "Glieise", 1.0)
    >>> dmap.add_distance("Glieise", "JFr14", 0.751)
    >>> p1 = Passenger("James Cameron", 2.0, "Earth", "Venus")
    >>> p1.give_distance(dmap)
    >>> p2 = Passenger("Catwell Romanuel", 1.0, "Glieise", "JFr14")
    >>> p2.give_distance(dmap)
    >>> _fare_bid(p1, p2)
    True
    >>> _fare_bid(p2, p1)
    False
    """
    return passenger_1.bid > passenger_2.bid


def _fare_per_dist(passenger_1: Passenger, passenger_2: Passenger) -> bool:
    """Return True iff passenger_1 has a higher fare_per_dist than
    passenger_2
    >>> dmap = DistanceMap()
    >>> dmap.add_distance("Earth", "Venus", 1.3)
    >>> dmap.add_distance("Venus", "Glieise", 1.0)
    >>> dmap.add_distance("Glieise", "JFr14", 0.751)
    >>> p1 = Passenger("James Cameron", 2.0, "Earth", "Venus")
    >>> p1.give_distance(dmap)
    >>> p2 = Passenger("Catwell Romanuel", 1.0, "Glieise", "JFr14")
    >>> p2.give_distance(dmap)
    >>> p3 = Passenger("Catwell Romanuel,,", 1.0, "Glieise", "Glieise")
    >>> p4 = Passenger("Catwell Romanuel.", 2.0, "JFr14", "JFr14")
    >>> _fare_per_dist(p1, p2)
    True
    >>> _fare_per_dist(p2, p1)
    False
    >>> _fare_per_dist(p1, p3)
    False
    >>> _fare_per_dist(p3, p1)
    True
    >>> _fare_per_dist(p2, p4)
    False
    >>> _fare_per_dist(p4, p2)
    True
    >>> _fare_per_dist(p3, p4)
    False
    >>> _fare_per_dist(p4, p3)
    True
    """
    p1_0 = passenger_1.source == passenger_1.destination
    p2_0 = passenger_2.source == passenger_2.destination
    both_0 = p1_0 and p2_0

    if both_0:
        return passenger_1.bid > passenger_2.bid
    elif p1_0:
        return True
    elif p2_0:
        return False
    else:
        return passenger_1.bid / passenger_1.distance >\
            passenger_2.bid / passenger_2.distance


def _sort_bikes_by_capacity(space_bikes: List[SpaceBike]) -> List[SpaceBike]:
    """Return a list of space bikes sorted by their capacity starting with the
    smallest and ending with the largest
    >>> sb1 = SpaceBike(198761, 'Nova Bike', 20, 8.0, 0.5)
    >>> sb2 = SpaceBike(198762, 'Nova Bike', 1, 8.0, 0.5)
    >>> sb3 = SpaceBike(198763, 'Nova Bike', 0, 8.0, 0.5)
    >>> sb4 = SpaceBike(198764, 'Nova Bike', 10, 8.0, 0.5)
    >>> sb5 = SpaceBike(198765, 'Nova Bike', 20, 8.0, 0.5)
    >>> sb_list = [sb1, sb2, sb3, sb4, sb5]
    >>> sorted_list = _sort_bikes_by_capacity(sb_list)
    >>> sorted_list[0].id
    198763
    >>> sorted_list[1].id
    198762
    >>> sorted_list[2].id
    198764
    >>> sorted_list[3].id
    198761
    >>> sorted_list[4].id
    198765
    """
    space_bikes_list = space_bikes.copy()  # make a shallow copy of the list
    distance_to_bike = {}
    distance_list = []
    for bike in space_bikes_list:  # loop through bikes
        if bike.curr_capacity not in distance_to_bike:
            distance_to_bike[bike.curr_capacity] = [bike]
            distance_list.append(bike.curr_capacity)
        else:
            distance_to_bike[bike.curr_capacity].append(bike)

    distance_list.sort()

    distance_to_bike_new = {}
    for distance in distance_list:
        distance_to_bike_new[distance] = distance_to_bike[distance]

    sorted_space_bikes = []
    for distance in distance_to_bike_new:
        for space_bike in distance_to_bike_new[distance]:
            sorted_space_bikes.append(space_bike)

    return sorted_space_bikes


def _check_enroute(passenger: Passenger, space_bike: SpaceBike) ->\
        Union[bool, str]:
    """Return True iff the space_bike is travelling through passenger's
    source and destination

    >>> dmap = DistanceMap()
    >>> dmap.add_distance("Earth", "Glieise", 0.4)
    >>> dmap.add_distance("Glieise", "J3Fr14", 0.4)
    >>> dmap.add_distance("J3Fr14", "V3Nus", 0.5)
    >>> dmap.add_distance("V3Nus", "Leaflet", 0.6)

    >>> sb = SpaceBike(198761, 'Nova Bike', 20, 8.0, 0.5)

    >>> p1 = Passenger("Leafletson,", 1.0, "Earth", "Glieise")
    >>> _check_enroute(p1, sb)  # sb only has default source route
    'Add destination'

    >>> sb.travel_chart = [("Earth", "Glieise",), ("Glieise", "J3Fr14",), \
    ("J3Fr14", "V3Nus",), ("V3Nus", "Leaflet",)]

    >>> p2 = Passenger("John Samdamns", 1.0, "Earth", "V3Nus")
    >>> p3 = Passenger("Laurey Platihominab,", 1.0, "Glieise", "V3Nus")
    >>> p4 = Passenger("Supreme,", 1.0, "Glieise", "Leaflet")
    >>> p5 = Passenger("Oktayion,", 1.0, "Earth", "Leaflet")
    >>> p6 = Passenger("KArrion 4ril,", 1.0, "Leaflet", "Earth")
    >>> p7 = Passenger("Iwanttocheck", 1.0, "V3Nus", "Leaflet")
    >>> p8 = Passenger("Iwanttocheck,", 1.0, "4drant", "Leaflet")
    >>> p9 = Passenger("Iwanttocheck, Uhgin", 1.0, "Glieise", "Earth")
    >>> p10 = Passenger("Fvk, Uuuu", 1.0, "Glieise", "Glieise")
    >>> p11 = Passenger("Fvk, Uuuu Egin", 1.0, "Earth", "Earth")
    >>> p12 = Passenger("Dontwanttocheck", 1.0, "V3Nus", "V3Nus")
    >>> p13 = Passenger("Dontwanttocheckatall", 1.0, "Leaflet", "Leaflet")
    >>> p14 = Passenger("Dontwanttocheckatall,,", 1.0, "Moranus", "Moranus")

    >>> _check_enroute(p1, sb)
    True
    >>> _check_enroute(p2, sb)
    True
    >>> _check_enroute(p3, sb)
    True
    >>> _check_enroute(p4, sb)
    True
    >>> _check_enroute(p5, sb)
    True
    >>> _check_enroute(p6, sb)
    'Add destination'
    >>> _check_enroute(p7, sb)
    True
    >>> _check_enroute(p8, sb)
    False
    >>> _check_enroute(p9, sb)
    'Add destination'
    >>> _check_enroute(p10, sb)
    True
    >>> _check_enroute(p11, sb)
    True
    >>> _check_enroute(p12, sb)
    True
    >>> _check_enroute(p13, sb)
    True
    >>> _check_enroute(p14, sb)
    False
    """
    source = passenger.source
    destination = passenger.destination
    source_present = False
    destination_present = False

    i = 0
    while i < len(space_bike.travel_chart):
        if source in space_bike.travel_chart[i]:
            source_present = True
            break
        i += 1

    if source_present:
        while i < len(space_bike.travel_chart):
            # for route in space_bike.travel_chart:
            if destination == space_bike.travel_chart[i][-1]:
                destination_present = True
            i += 1

    if not source_present:
        return False
    elif source_present and source == destination:
        return True
    elif source_present and not destination_present:
        return "Add destination"
    elif source_present and destination_present:
        return True


def _return_bike_enroute_poss_bikes(passenger: Passenger,
                                    sorted_sb_list: list) ->\
        Union[list, SpaceBike]:
    """Return a bicycle is passanger is enroute, otherwise, return a list of
    possible bicycles that could board passengers"""

    can_board = []
    i = 0
    while i < len(sorted_sb_list):
        if _check_enroute(passenger, sorted_sb_list[i]) != "Add destination" \
                and _check_enroute(passenger, sorted_sb_list[i]):
            return sorted_sb_list[i]  # return first bike that's enroute
        elif _check_enroute(passenger, sorted_sb_list[i]) == "Add destination":
            can_board.append(sorted_sb_list[i])  # create list of possible bikes
        i += 1

    return can_board


def _sb_priority_fuel(passenger: Passenger, distance_map: DistanceMap,
                      can_board: list) -> Union[None, SpaceBike, list]:
    """Return None if no space bikes are available, or return a spacebike or a
    list of spacebikes possible for boarding"""

    # compare can_board bikes to see which will take the least fuel
    fuel_to_bike = {}
    fuel_list = []
    for bike in can_board:
        # last location on bike route and passenger destination
        new_route = (bike.travel_chart[-1][-1], passenger.destination,)
        if bike.get_fuel_needed(new_route, distance_map) not in \
                fuel_to_bike:  # create a new dict object
            fuel_to_bike[bike.get_fuel_needed(new_route, distance_map)] = [bike]
            # append fuel to fuel_list
            fuel_list.append(bike.get_fuel_needed(new_route, distance_map))
        else:  # append to the dict object
            fuel_to_bike[bike.get_fuel_needed(new_route, distance_map)] \
                .append(bike)

    if "Insufficient Fuel" in fuel_list:  # remove bikes with insufficient fuel
        fuel_list.remove("Insufficient Fuel")

    if len(fuel_list) > 0:
        least_fuel = min(fuel_list)
    else:
        return None

    can_board_fuel = fuel_to_bike[least_fuel]  # list

    if len(can_board_fuel) == 1:
        return can_board_fuel[0]
    elif len(can_board_fuel) == 0:
        return None

    return can_board_fuel


def _sb_priority_capacity(can_board_fuel: list) -> \
        Union[None, SpaceBike, list]:
    """Do same as previous, just for capacity"""
    # pick bike with least available capacity
    capacity_to_bike = {}
    capacity_list = []
    for bike in can_board_fuel:
        # last location on bike route and passenger destination
        capacity = bike.curr_capacity
        if capacity not in capacity_to_bike:  # create a new dict object
            capacity_to_bike[capacity] = [bike]
            # append fuel to fuel_list
            capacity_list.append(capacity)
        else:  # append to the dict object
            capacity_to_bike[capacity].append(bike)

    if 0 in capacity_list:  # remove bikes with insufficient capacity
        capacity_list.remove(0)

    if len(capacity_list) > 0:
        least_capacity = min(capacity_list)
    else:
        return None

    can_board_capacity = capacity_to_bike[least_capacity]

    if len(can_board_capacity) == 1:
        return can_board_capacity[0]
    elif len(can_board_capacity) == 0:
        return None

    return can_board_capacity


def _space_bike_priority(passenger: Passenger,
                         space_bikes: List[SpaceBike],
                         distance_map: DistanceMap) \
        -> Optional[SpaceBike]:
    """Return a space_bike that can board passenger, or return None, if no space
    bike meets the criteria"""
    sorted_sb_list = _sort_bikes_by_capacity(space_bikes)
    sorted_sb_list_copy = sorted_sb_list.copy()

    for bike in sorted_sb_list_copy:  # remove space_bikes with 0 capacity
        if bike.curr_capacity < 1:
            sorted_sb_list.remove(bike)

    can_board = _return_bike_enroute_poss_bikes(passenger, sorted_sb_list)
    if isinstance(can_board, SpaceBike):
        return can_board

    can_board_fuel = _sb_priority_fuel(passenger, distance_map, can_board)
    if can_board_fuel is None or isinstance(can_board_fuel, SpaceBike):
        return can_board_fuel

    can_board_capacity = _sb_priority_capacity(can_board_fuel)
    if can_board_capacity is None or isinstance(can_board_capacity, SpaceBike):
        return can_board_capacity

    # pick bike with the smallest ID
    id_to_bike = {}
    id_list = []
    for bike in can_board_capacity:
        # last location on bike route and passenger destination
        id_ = bike.id
        if id_ not in id_to_bike:  # create a new dict object
            id_to_bike[id_] = [bike]
            # append fuel to fuel_list
            id_list.append(id_)
        else:  # append to the dict object
            id_to_bike[id_].append(bike)

    if len(id_list) > 0:
        least_id = min(id_list)
    else:
        return None

    chosen_bike = id_to_bike[least_id][0]

    return chosen_bike


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'allowed-io': ['compare_algorithms'],
        'allowed-import-modules': [
            'doctest', 'python_ta', 'typing',
            'random', 'container', 'domain',
            'a2_space_bikes', 'a2_container', 'a2_distance_map'
        ],
        'max-attributes': 15,
        'disable': ['E1136']
    })
