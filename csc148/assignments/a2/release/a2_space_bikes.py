"""Assignment 2 - SpaceBikes, Passengers, and SpaceFleets.

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

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 the Department of Computer Science,
University of Toronto

===== Module Description =====

This module contains the Passenger, SpaceBike, and SpaceFleet
classes.
"""

from typing import List, Dict, Tuple, Union
from a2_distance_map import DistanceMap

DEFAULT_STARTING_LOC = 'Earth'
FUEL_COST_PER_UNIT = 0.75


class Passenger:
    """A Passenger

    === Public Attributes ===
    name:
      The name of the passenger
    bid:
      The amount of the bid made by the passenger
    source:
      Where the passenger wishes to be picked up
    destination:
      Where the passenger wishes to be dropped
    distance:
      The distance between source and destination locations gotten
      from a distance map
    """

    name: str
    bid: float
    source: str
    destination: str
    distance: float

    def __init__(self, name: str, bid: float, source: str, destination: str) ->\
            None:
        """Initialise an instance of Passenger"""

        self.name = name
        self.bid = bid
        self.source = source
        self.destination = destination
        self.distance = None

    def give_distance(self, distance_map: DistanceMap) -> None:
        """Return the distance between passenger source and destination

        >>> dmap = DistanceMap()
        >>> dmap.add_distance("Earth", "Venus", 0.4)
        >>> p1 = Passenger("Jeffery Flambuya", 1.0, "Earth", "Venus")
        >>> p1.give_distance(dmap)
        >>> p1.distance
        0.4
        """
        if self.source == self.destination:
            self.distance = 0
            return

        travel_route = (self.source, self.destination,)
        distance = distance_map.map_()[travel_route]
        self.distance = distance


class SpaceBike:
    """A Space Bike

    === Public Attributes ===
    id:
      id
    bike_type:
      the type of the bike
    max_capacity:
      the maximum number of passengers the bike could carry
    curr_capacity:
      the number of passengers the bike can currently carry
    max_fuel_capacity:
      the maximum amount of fuel a bike can contain
    fuel_level:
      the current amount of fuel a bike holds
    fuel_usage_rate:
      the rate at which fuel is used
    passenger_list:
      list of passengers boarded on bike
    passenger_name_list:
      list of passenger names
    starting_location:
      starting location of the bike
    fare_collected:
      the total amount of fare collected from boarded passengers
    travel_chart:
      a list of the routes each bike has to take(no repeats)
    base_opt_cost:
      the base operational cost of the bike
    """

    id: int
    bike_type: str
    max_capacity: int
    curr_capacity: int
    max_fuel_capacity: float
    fuel_level: float
    fuel_usage_rate: float
    passenger_list: List[Passenger]
    passenger_name_list: List[str]
    starting_location: str
    fare_collected: int
    travel_chart: List[Tuple[str]]
    base_opt_cost: float

    def __init__(self, id_: int, bike_types: str, max_capacity: int,
                 max_fuel_capacity: float, fuel_usage_rate: float,
                 starting_location: str = DEFAULT_STARTING_LOC) -> None:
        """Initialise an instance of Space Bike"""

        self.id = id_
        self.bike_type = bike_types
        self.max_capacity = max_capacity
        self.curr_capacity = max_capacity
        self.max_fuel_capacity = max_fuel_capacity
        self.fuel_level = max_fuel_capacity
        self.fuel_usage_rate = fuel_usage_rate
        self.passenger_list = []
        self.passenger_name_list = []
        self.starting_location = starting_location
        self.fare_collected = 0
        self.travel_chart = [(DEFAULT_STARTING_LOC,)]

        if bike_types == 'Atom Bike':
            self.base_opt_cost = 1.2
        elif bike_types == 'Nova Bike':
            self.base_opt_cost = 2.4
        elif bike_types == 'MC^2 Bike':
            self.base_opt_cost = 10.1
        else:
            raise TypeError

    def _route_distance(self, distance_map: DistanceMap) -> float:
        """Return the total distance this bike will travel on it's current
        route
        >>> dmap = DistanceMap()
        >>> dmap.add_distance("Earth", "Mars", 0.4)
        >>> dmap.add_distance("Mars", "Gliese", 0.4)
        >>> sb = SpaceBike(198761, 'Nova Bike', 20, 8.0, 0.5)
        >>> p1 = Passenger("Jeff Connor", 1.0, "Earth", "Mars")
        >>> p4 = Passenger("Sandra Corgei", 1.0, "Mars", "Gliese")
        >>> sb.board(p1, dmap)
        True
        >>> sb.board(p4, dmap)
        True
        >>> sb._route_distance(dmap)
        0.8
        """
        distance = 0
        for route in self.travel_chart:
            map_ = distance_map.map_()
            if route in map_:
                distance += map_[route]
        return distance

    def public_route_distance(self, distance_map: DistanceMap) -> float:
        """Calls the private _route_distance method and returns the result
        >>> dmap = DistanceMap()
        >>> dmap.add_distance("Earth", "Mars", 0.4)
        >>> dmap.add_distance("Mars", "Gliese", 0.4)
        >>> sb = SpaceBike(198761, 'Nova Bike', 20, 8.0, 0.5)
        >>> p1 = Passenger("Jeff Connor", 1.0, "Earth", "Mars")
        >>> p4 = Passenger("Sandra Corgei", 1.0, "Mars", "Gliese")
        >>> sb.board(p1, dmap)
        True
        >>> sb.board(p4, dmap)
        True
        >>> sb.public_route_distance(dmap)
        0.8
        """
        return self._route_distance(distance_map)

    def _check_fuel(self, travel_route: Tuple[str], distance_map: DistanceMap)\
            -> bool:
        """Return True if Space Bike has enough fuel to also fly through
        travel route, return False, otherwise
        >>> dmap = DistanceMap()
        >>> dmap.add_distance("Earth", "Mars", 0.4)
        >>> dmap.add_distance("Mars", "Gliese", 0.4)
        >>> dmap.add_distance("Gliese", "Jupiter", 100)
        >>> sb = SpaceBike(198761, 'Nova Bike', 20, 8.0, 0.5)
        >>> p1 = Passenger("Jeff Connor", 1.0, "Earth", "Mars")
        >>> p4 = Passenger("Sandra Corgei", 1.0, "Mars", "Gliese")
        >>> sb.board(p1, dmap)
        True
        >>> sb.board(p4, dmap)
        True
        >>> sb._route_distance(dmap)
        0.8
        >>> new_travel_route = ("Gliese", "Jupiter",)
        >>> sb._check_fuel(new_travel_route, dmap)
        False
        """
        if travel_route[0] == travel_route[-1]:
            return True
        distance = self._route_distance(distance_map)
        new_route_dist = distance_map.map_()[travel_route]
        possible_distance = distance + new_route_dist
        return (possible_distance * self.fuel_usage_rate) <=\
            self.fuel_level

    def get_fuel_needed(self, travel_route: Tuple[str],
                        distance_map: DistanceMap) -> Union[str, float]:
        """Return the amount of fuel space_bike needs to fly from the last
        destination on it's map to the new
        >>> dmap = DistanceMap()
        >>> dmap.add_distance("Earth", "Mars", 0.4)
        >>> dmap.add_distance("Mars", "Gliese", 0.4)
        >>> dmap.add_distance("Gliese", "Jupiter", 100)
        >>> sb = SpaceBike(198761, 'Nova Bike', 20, 8.0, 0.5)
        >>> p1 = Passenger("Jeff Connor", 1.0, "Earth", "Mars")
        >>> p4 = Passenger("Sandra Corgei", 1.0, "Mars", "Gliese")
        >>> sb.board(p1, dmap)
        True
        >>> sb.board(p4, dmap)
        True
        >>> sb._route_distance(dmap)
        0.8
        >>> new_travel_route = ("Gliese", "Jupiter",)
        >>> sb.get_fuel_needed(new_travel_route, dmap)
        'Insufficient Fuel'
        """
        distance = self._route_distance(distance_map)
        new_route_dist = distance_map.map_()[travel_route]
        if ((distance + new_route_dist) * self.fuel_usage_rate) <=\
                self.fuel_level:
            return new_route_dist * self.fuel_usage_rate
        else:
            return "Insufficient Fuel"

    def _board_same_dists(self, passenger: Passenger) -> bool:
        """Board passenger's with the same source and destination, when the
        passenger has it's source in the bike's travel chart"""
        if passenger not in self.passenger_list and self.curr_capacity > 0:
            self.passenger_list.append(passenger)
            self.passenger_name_list.append(passenger.name)
            self.fare_collected += passenger.bid
            self.curr_capacity -= 1
            return True
        else:
            return False

    def board(self, passenger: Passenger, distance_map: DistanceMap) -> bool:
        """Board passenger on bike, by appending passenger to passenger
         list, and return True if successful, otherwise, return false

         >>> dmap = DistanceMap()
         >>> dmap.add_distance("Earth", "Mars", 0.4)
         >>> dmap.add_distance("Mars", "Gliese", 0.4)
         >>> sb = SpaceBike(198761, 'Nova Bike', 4, 8.0, 0.5)
         >>> p0 = Passenger("Fvk U Alot", 1.0, "Earth", "Earth")
         >>> p1 = Passenger("Jeff Connor", 1.0, "Earth", "Mars")
         >>> p2 = Passenger("Al Frank", 1.0, "Earth", "Mars")
         >>> p3 = Passenger("Jeff Connor", 1.0, "Jupiter", "Neptune")
         >>> p4 = Passenger("Sandra Corgei", 1.0, "Mars", "Gliese")
         >>> p5 = Passenger("Sandra,", 1.0, "Mars", "Gliese")  # test no space
         >>> sb.num_passengers()
         0
         >>> sb.board(p0, dmap)
         True
         >>> len(sb.travel_chart)
         1
         >>> sb.curr_capacity
         3
         >>> sb.board(p2, dmap)
         True
         >>> sb.curr_capacity
         2
         >>> sb.board(p2, dmap)
         False
         >>> sb.num_passengers()
         2
         >>> sb.passenger_name_list
         ['Fvk U Alot', 'Al Frank']
         >>> sb.fare_collected
         2.0
         >>> sb.travel_chart
         [('Earth', 'Mars')]
         >>> sb.board(p1, dmap)
         True
         >>> sb.curr_capacity
         1
         >>> sb.travel_chart
         [('Earth', 'Mars')]
         >>> sb.board(p3, dmap)
         False
         >>> sb.travel_chart
         [('Earth', 'Mars')]
         >>> sb.board(p4, dmap)
         True
         >>> sb.curr_capacity
         0
         >>> sb.travel_chart
         [('Earth', 'Mars'), ('Mars', 'Gliese')]
         >>> sb.board(p5, dmap)
         False
         >>> sb.travel_chart
         [('Earth', 'Mars'), ('Mars', 'Gliese')]
         >>> dmap2 = DistanceMap()
         >>> dmap2.add_distance("Earth", "Mars", 0.4)
         >>> sb2 = SpaceBike(198761, 'Nova Bike', 4, 8.0, 0.5)
         >>> sb2.travel_chart = [('Earth', 'Mars')]
         >>> p7 = Passenger("Sandra,", 1.0, "Earth", "Mars")
         >>> sb2.board(p7, dmap2)
         True
         >>> sb2.travel_chart == [('Earth', 'Mars')]
         True
         """
        i = 0
        len_chart = len(self.travel_chart)
        # checks if passenger.source is a destination on bike travel route
        while i < len_chart and \
                passenger.source not in self.travel_chart[i]:
            i += 1

        # return false if passenger source not in travel route
        if i >= len_chart:
            return False

        # this is where _board_same_dist
        if passenger.source == passenger.destination:
            return self._board_same_dists(passenger)

        # the next pair added to travel route will be bike's last
        # destination and passenger destination
        appended_travel_route = (self.travel_chart[-1][-1],
                                 passenger.destination,)
        # ensure that appended_travel_route is not a repetition of destinations
        if appended_travel_route[0] == appended_travel_route[1]:
            appended_travel_route = (passenger.source, passenger.destination,)
        # checks if passenger route already on bike.travel_chart, and checks if
        # passenger.source is in bike.travel_chart by checking if i < len_chart
        if passenger not in self.passenger_list and i < len_chart and \
                self._check_fuel(appended_travel_route, distance_map)\
                and self.curr_capacity > 0:
            self.passenger_list.append(passenger)
            self.passenger_name_list.append(passenger.name)
            self.fare_collected += passenger.bid
            self.curr_capacity -= 1

            # checks if self.travel_chart has the DEFAULT_STARTING_LOC source
            # as its only travel route
            if i == 0 and len(self.travel_chart[0]) == 1:
                travel_route = (DEFAULT_STARTING_LOC, passenger.destination,)
                self.travel_chart[0] = travel_route
                return True
            else:
                # otherwise, a new travel route pair should be added to
                # self.travel_chart
                travel_route = (passenger.source, passenger.destination,)
                # checks if travel_route is already in travel_chart
                if travel_route not in self.travel_chart:
                    self.travel_chart.append(appended_travel_route)
            return True
        # if passenger.source not in travel_chart
        # if bike does not have enough fuel for flight
        return False

    def num_passengers(self) -> int:
        """Return the number of passengers on bike

        >>> dmap = DistanceMap()
        >>> dmap.add_distance("Earth", "Mars", 0.4)
        >>> sb = SpaceBike(198761, 'Nova Bike', 20, 8.0, 0.5)
        >>> p2 = Passenger("Al Frank", 1.0, "Earth", "Mars")
        >>> sb.num_passengers()
        0
        >>> sb.board(p2, dmap)
        True
        >>> sb.num_passengers()
        1
        """
        return len(self.passenger_list)

    def is_empty(self) -> bool:
        """Return True if the bike has no boarded passengers

        >>> dmap = DistanceMap()
        >>> dmap.add_distance("Earth", "Mars", 0.4)
        >>> sb = SpaceBike(198761, 'Nova Bike', 20, 8.0, 0.5)
        >>> p2 = Passenger("Al Frank", 1.0, "Earth", "Mars")
        >>> sb.num_passengers()
        0
        >>> sb.is_empty()
        True
        >>> sb.board(p2, dmap)
        True
        >>> sb.num_passengers()
        1
        >>> sb.is_empty()
        False
        """

        if len(self.passenger_list) == 0:
            return True
        else:
            return False


class SpaceFleet:
    """A Fleet of SpaceBikes for intergalactic travel.

    === Public Attributes ===
    bikes:
      List of all SpaceBike objects in this SpaceFleet

    """
    bikes: List[SpaceBike]

    def __init__(self) -> None:
        """Create a SpaceFleet with no bikes.

        >>> sf = SpaceFleet()
        >>> sf.num_space_bikes()
        0
        """
        self.bikes = []

    def add_space_bike(self, space_bike: SpaceBike) -> None:
        """Add space_bike to this SpaceFleet.

        Precondition: No other space_bike with the same ID as
        space_bike has already been added to this Fleet.

        >>> sf = SpaceFleet()
        >>> sb = SpaceBike(198761, 'Nova Bike', 20, 8.0, 0.5)
        >>> sf.add_space_bike(sb)
        >>> sf.num_space_bikes()
        1
        """
        self.bikes.append(space_bike)

    def num_space_bikes(self) -> int:
        """Return the number of bikes in this SpaceFleet.

        >>> sf = SpaceFleet()
        >>> sf.num_space_bikes()
        0
        >>> sb = SpaceBike(198761, 'Nova Bike', 20, 8.0, 0.5)
        >>> sf.add_space_bike(sb)
        >>> sf.num_space_bikes()
        1
        """
        return len(self.bikes)

    def num_nonempty_bikes(self) -> int:
        """Return the number of SpaceBikes that are not empty.

        >>> sf = SpaceFleet()
        >>> b1 = SpaceBike(198161, 'Nova Bike', 20, 8.0, 0.5)
        >>> b2 = SpaceBike(198761, 'Nova Bike', 20, 8.0, 0.5)
        >>> b3 = SpaceBike(198561, 'Nova Bike', 20, 8.0, 0.5)
        >>> sf.add_space_bike(b1)
        >>> sf.add_space_bike(b2)
        >>> sf.add_space_bike(b3)
        >>> p1 = Passenger("Al Roger", 1.0, "Earth", "Mars")
        >>> dmap = DistanceMap()
        >>> dmap.add_distance("Earth", "Mars", 0.4)
        >>> b1.board(p1, dmap)
        True
        >>> sf.num_nonempty_bikes()
        1
        >>> p2 = Passenger("Al Frank", 1.0, "Earth", "Mars")
        >>> b2.board(p2, dmap)
        True
        >>> sf.num_nonempty_bikes()
        2
        """
        count = 0
        for bike in self.bikes:
            if bike.num_passengers() > 0:
                count += 1
        return count

    def passenger_placements(self) -> Dict[int, List[str]]:
        """Return a dictionary in which each key is the ID of a SpaceBike
        in this fleet and its value is a list of the passengers on board
        the SpaceBike, in the order that they boarded.

        >>> sf = SpaceFleet()
        >>> b1 = SpaceBike(198161, 'Nova Bike', 20, 8.0, 0.5)
        >>> b2 = SpaceBike(198761, 'Nova Bike', 20, 8.0, 0.5)
        >>> b3 = SpaceBike(198561, 'Nova Bike', 20, 8.0, 0.5)
        >>> sf.add_space_bike(b1)
        >>> sf.add_space_bike(b2)
        >>> sf.add_space_bike(b3)
        >>> p1 = Passenger("Al Roger", 1.0, "Earth", "Mars")
        >>> dmap = DistanceMap()
        >>> dmap.add_distance("Earth", "Mars", 0.4)
        >>> b1.board(p1, dmap)
        True
        >>> p2 = Passenger("Al Frank", 1.0, "Earth", "Mars")
        >>> b2.board(p2, dmap)
        True
        >>> p3 = Passenger("Anne Rose", 1.0, "Earth", "Mars")
        >>> b2.board(p3, dmap)
        True
        >>> sf.passenger_placements() == {
        ...     198161: ["Al Roger"],
        ...     198761: ["Al Frank", "Anne Rose"],
        ...     198561: []
        ... }
        True
        """
        bike_dict = {}
        for bike in self.bikes:
            bike_dict[bike.id] = bike.passenger_name_list

        return bike_dict

    def vacant_seats(self) -> int:
        """Return the total number of seats available across all *non-empty*
        SpaceBikes in the SpaceFleet.

        If there are no non-empty SpaceBikes in the SpaceFleet, return 0.

        >>> sf = SpaceFleet()
        >>> b1 = SpaceBike(198161, 'Nova Bike', 20, 8.0, 0.5)
        >>> b2 = SpaceBike(198761, 'Nova Bike', 20, 8.0, 0.5)
        >>> b3 = SpaceBike(198561, 'Nova Bike', 20, 8.0, 0.5)
        >>> sf.add_space_bike(b1)
        >>> sf.add_space_bike(b2)
        >>> sf.add_space_bike(b3)
        >>> p1 = Passenger("Al Roger", 1.0, "Earth", "Mars")
        >>> dmap = DistanceMap()
        >>> dmap.add_distance("Earth", "Mars", 0.4)
        >>> b1.board(p1, dmap)
        True
        >>> p2 = Passenger("Al Frank", 1.0, "Earth", "Mars")
        >>> b2.board(p2, dmap)
        True
        >>> p3 = Passenger("Anne Rose", 1.0, "Earth", "Mars")
        >>> b2.board(p3, dmap)
        True
        >>> sf.vacant_seats()
        37

        """
        count = 0
        for bike in self.bikes:
            if bike.num_passengers() > 0:
                count += bike.max_capacity - bike.num_passengers()

        return count

    def total_fare_collected(self) -> float:
        """Return the total amount of fare collected from all
        Passengers on board all SpaceBikes in this SpaceFleet.

        >>> sf = SpaceFleet()
        >>> b1 = SpaceBike(198161, 'Nova Bike', 20, 8.0, 0.5)
        >>> b2 = SpaceBike(198761, 'Nova Bike', 20, 8.0, 0.5)
        >>> b3 = SpaceBike(198561, 'Nova Bike', 20, 8.0, 0.5)
        >>> sf.add_space_bike(b1)
        >>> sf.add_space_bike(b2)
        >>> sf.add_space_bike(b3)
        >>> p1 = Passenger("Al Roger", 1.0, "Earth", "Mars")
        >>> dmap = DistanceMap()
        >>> dmap.add_distance("Earth", "Mars", 0.4)
        >>> b1.board(p1, dmap)
        True
        >>> p2 = Passenger("Al Frank", 1.0, "Earth", "Mars")
        >>> b2.board(p2, dmap)
        True
        >>> p3 = Passenger("Anne Rose", 1.0, "Earth", "Mars")
        >>> b2.board(p3, dmap)
        True
        >>> sf.total_fare_collected() == 3.0
        True
        """
        total_fare = 0
        for bike in self.bikes:
            total_fare += bike.fare_collected

        return total_fare

    def total_distance_travelled(self, dmap: DistanceMap) -> float:
        """Return the total distance travelled across all SpaceBikes
        in this SpaceFleet.

        The distance travelled is calculated for each SpaceBike according
        to their route and <dmap>.

        >>> sf = SpaceFleet()
        >>> b1 = SpaceBike(198161, 'Nova Bike', 20, 8.0, 0.5)
        >>> b2 = SpaceBike(198761, 'Nova Bike', 20, 8.0, 0.5)
        >>> b3 = SpaceBike(198561, 'Nova Bike', 20, 8.0, 0.5)
        >>> sf.add_space_bike(b1)
        >>> sf.add_space_bike(b2)
        >>> sf.add_space_bike(b3)
        >>> p1 = Passenger("Al Roger", 1.0, "Earth", "Mars")
        >>> dmap = DistanceMap()
        >>> dmap.add_distance("Earth", "Mars", 0.4)
        >>> b1.board(p1, dmap)
        True
        >>> p2 = Passenger("Al Frank", 1.0, "Earth", "Mars")
        >>> b2.board(p2, dmap)
        True
        >>> p3 = Passenger("Anne Rose", 1.0, "Earth", "Mars")
        >>> b2.board(p3, dmap)
        True
        >>> sf.total_distance_travelled(dmap) == 0.8
        True
        """
        distance = 0
        for bike in self.bikes:
            if not bike.is_empty():
                distance += bike.public_route_distance(dmap)
        return distance

    def _total_passenger_count(self) -> int:
        """Return the total number of passengers boarded
        across all SpaceBikes in this SpaceFleet.

        >>> sf = SpaceFleet()
        >>> b1 = SpaceBike(198161, 'Nova Bike', 20, 8.0, 0.5)
        >>> b2 = SpaceBike(198761, 'Nova Bike', 20, 8.0, 0.5)
        >>> b3 = SpaceBike(198561, 'Nova Bike', 20, 8.0, 0.5)
        >>> sf.add_space_bike(b1)
        >>> sf.add_space_bike(b2)
        >>> sf.add_space_bike(b3)
        >>> p1 = Passenger("Al Roger", 1.0, "Earth", "Mars")
        >>> dmap = DistanceMap()
        >>> dmap.add_distance("Earth", "Mars", 0.4)
        >>> b1.board(p1, dmap)
        True
        >>> p2 = Passenger("Al Frank", 1.0, "Earth", "Mars")
        >>> b2.board(p2, dmap)
        True
        >>> p3 = Passenger("Anne Rose", 1.0, "Earth", "Mars")
        >>> b2.board(p3, dmap)
        True
        >>> sf._total_passenger_count()
        3
        """
        num_passengers = 0
        for bike in self.bikes:
            num_passengers += bike.num_passengers()
        return num_passengers

    def average_fill_percent(self) -> float:
        """Return the average fill percent across all SpaceBikes in
        this SpaceFleet.

        Precondition:
        - there is at least one SpaceBike in the SpaceFleet.

        >>> sf = SpaceFleet()
        >>> b1 = SpaceBike(198161, 'Nova Bike', 20, 8.0, 0.5)
        >>> b2 = SpaceBike(198761, 'Nova Bike', 20, 8.0, 0.5)
        >>> b3 = SpaceBike(198561, 'Nova Bike', 20, 8.0, 0.5)
        >>> sf.add_space_bike(b1)
        >>> sf.add_space_bike(b2)
        >>> sf.add_space_bike(b3)
        >>> p1 = Passenger("Al Roger", 1.0, "Earth", "Mars")
        >>> dmap = DistanceMap()
        >>> dmap.add_distance("Earth", "Mars", 0.4)
        >>> b1.board(p1, dmap)
        True
        >>> p2 = Passenger("Al Frank", 1.0, "Earth", "Mars")
        >>> b2.board(p2, dmap)
        True
        >>> p3 = Passenger("Anne Rose", 1.0, "Earth", "Mars")
        >>> b2.board(p3, dmap)
        True
        >>> # b1: 1/20, b2: 2/20, b3: 0/20
        >>> # 100 * (1/20 + 2/20 + 0/20) / 3 = 5
        >>> eps = 0.0001  # floating point error tolerance
        >>> abs(sf.average_fill_percent() - 5) < eps
        True
        """
        total_fraction = 0
        for bike in self.bikes:
            total_fraction += bike.num_passengers() / bike.max_capacity

        percentage = 100 * total_fraction / len(self.bikes)
        return percentage

    def average_distance_travelled(self, dmap: DistanceMap) -> float:
        """Return the average distance travelled across all **non-empty**
        SpaceBikes in this SpaceFleet.

        The average distance travelled is defined as the total distance
        travelled divided by the number of **non-empty** SpaceBikes in the
        SpaceFleet.

        Precondition:
          - There is at least one non-empty SpaceBike in this SpaceFleet.

        >>> sf = SpaceFleet()
        >>> b1 = SpaceBike(198161, 'Nova Bike', 20, 8.0, 0.5)
        >>> b2 = SpaceBike(198761, 'Nova Bike', 20, 8.0, 0.5)
        >>> b3 = SpaceBike(198561, 'Nova Bike', 20, 8.0, 0.5)
        >>> sf.add_space_bike(b1)
        >>> sf.add_space_bike(b2)
        >>> sf.add_space_bike(b3)
        >>> p1 = Passenger("Al Roger", 1.0, "Earth", "Mars")
        >>> dmap = DistanceMap()
        >>> dmap.add_distance("Earth", "Mars", 0.4)
        >>> b1.board(p1, dmap)
        True
        >>> p2 = Passenger("Al Frank", 1.0, "Earth", "Mars")
        >>> b2.board(p2, dmap)
        True
        >>> p3 = Passenger("Anne Rose", 1.0, "Earth", "Mars")
        >>> b2.board(p3, dmap)
        True
        >>> sf.average_distance_travelled(dmap) # b3 is empty, do not include
        0.4
        """
        avg_dist = self.total_distance_travelled(dmap) \
            / self.num_nonempty_bikes()
        return avg_dist

    def total_deployment_cost(self, dmap: DistanceMap) -> float:
        """Return the total deployment cost for deploying all **non-empty**
        SpaceBikes in the fleet.

        The deployment cost is defined as the sum of the base cost of
        operation (see A2 handout) and the total fuel cost. The total fuel
        cost for a single space bike is the total fuel expended by its route,
        multiplied by the FUEL_COST_PER_UNIT constant.

        >>> sf = SpaceFleet()
        >>> b1 = SpaceBike(198161, 'Nova Bike', 20, 8.0, 0.5)
        >>> b2 = SpaceBike(198761, 'Nova Bike', 20, 8.0, 0.5)
        >>> b3 = SpaceBike(198561, 'Nova Bike', 20, 8.0, 0.5)
        >>> sf.add_space_bike(b1)
        >>> sf.add_space_bike(b2)
        >>> sf.add_space_bike(b3)
        >>> p1 = Passenger("Al Roger", 1.0, "Earth", "Mars")
        >>> dmap = DistanceMap()
        >>> dmap.add_distance("Earth", "Mars", 0.4)
        >>> b1.board(p1, dmap)
        True
        >>> p2 = Passenger("Al Frank", 1.0, "Earth", "Mars")
        >>> b2.board(p2, dmap)
        True
        >>> p3 = Passenger("Anne Rose", 1.0, "Earth", "Mars")
        >>> b2.board(p3, dmap)
        True
        >>> sf.total_deployment_cost(dmap)
        5.1
        """
        cost = 0

        for bike in self.bikes:
            if not bike.is_empty():
                cost += bike.base_opt_cost
                for route in bike.travel_chart:
                    distance = _get_distance__(route, dmap)
                    cost += bike.fuel_usage_rate * distance \
                        * FUEL_COST_PER_UNIT

        return cost


def _get_distance__(route: Tuple[str], dmap: DistanceMap) \
        -> int:
    """Return distance of route <route> from distance map<distance_map>"""
    if len(route) == 1 and route[0] == DEFAULT_STARTING_LOC:
        distance = 0
    else:
        distance = dmap.map_()[route]
    return distance


if __name__ == "__main__":
    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': [
            'doctest', 'python_ta', 'typing', 'a2_distance_map'
        ],
        'max-attributes': 15,
        'max-args': 15,
        'disable': ['E1136']
    })

    import doctest
    doctest.testmod()
