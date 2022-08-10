"""Assignment 2 - Distance map [Task 1]

CSC148, Summer 2021

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

This module is replicated with permission from the Winter 2021 A1,
created by Diane Horton, Ian Berlott-Attwell, Jonathan Calver,
Sophia Huynh, Maryam Majedi, and Jaisie Sin.

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 the Department of Computer Science,
University of Toronto

===== Module Description =====

This module contains the class DistanceMap, which is used to store
and look up distances between intergalactic bodies. This class does not
read distances from the map file. (All reading from files is done in module
a2_command_central.)

Instead, it provides public methods that can be called to store and look up
distances.

"""

from typing import Dict, Tuple


class DistanceMap:
    """A Map showing the distance from one galaxy location to another

    === Private Attributes ===
    _map:
      a dictionary mapping travel routes to their travel distance
    """
    _map: Dict[Tuple[str], int]

    def __init__(self) -> None:
        """Initialises a new instance of class DistanceMap"""
        self._map = {}

    def add_distance(self, departure: str, destination: str, distance: float) \
            -> None:
        """Returns the distance from departure to destination

        ===Sample Usage===
        >>> map_ = DistanceMap()
        >>> map_.add_distance('A', 'B', 14.9)
        >>> map_.add_distance('B', 'A', 13.5)
        >>> map_.distance('A', 'B')
        14.9
        >>> map_.distance('B', 'A')
        13.5
        >>> map_.distance('C', 'A')
        -1.0
        """
        travel_route = (departure, destination,)
        travel_route_rev = (destination, departure,)

        self._map[travel_route] = distance

        if travel_route_rev not in self._map:
            self._map[travel_route_rev] = distance

    def distance(self, departure: str, destination: str) -> float:
        """Returns the distance from departure to destination

        ===Sample Usage===
        >>> map_ = DistanceMap()
        >>> map_.add_distance('A', 'B', 14.9)
        >>> map_.distance('B', 'A')
        14.9
        >>> map_.add_distance('B', 'A', 13.5)
        >>> map_.distance('A', 'B')
        14.9
        >>> map_.distance('B', 'A')
        13.5
        >>> map_.distance('C', 'A')
        -1.0
        """
        travel_route = (departure, destination,)
        if travel_route in self._map:
            return self._map[travel_route]
        else:
            return -1.0

    def map_(self) -> Dict[Tuple[str], int]:
        """Return self._map
        ===Sample Usage===
        >>> map_ = DistanceMap()
        >>> map_.add_distance('A', 'B', 14.9)
        >>> map_.distance('B', 'A')
        14.9
        >>> map_.add_distance('B', 'A', 13.5)
        >>> map_.map_()
        {('A', 'B'): 14.9, ('B', 'A'): 13.5}
        """
        map_ = self._map.copy()
        return map_


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': ['doctest', 'python_ta', 'typing'],
        'disable': ['E1136'],
        'max-attributes': 15
    })
    import doctest
    doctest.testmod()
