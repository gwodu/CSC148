from a2_space_bikes import SpaceFleet, SpaceBike, Passenger
from a2_container import PriorityQueue, _QueueNode
from a2_command_central import CommandCentral
from a2_distance_map import DistanceMap
from a2_fleet_scheduler import BogoScheduler, GreedyScheduler, _space_bike_priority, _sort_bikes_by_capacity, _sb_priority_capacity, _sb_priority_fuel, _return_bike_enroute_poss_bikes
import tempfile


def test_board_general():
    sb1 = SpaceBike(0, 'Atom Bike', 3, 3.81, 0.48)
    sb2 = SpaceBike(1, 'Nova Bike', 20, 7.54, 0.9)
    sb_list = [sb1, sb2]

    p1 = Passenger('Passenger 1', 96, 'Earth', 'Mercury')
    p6 = Passenger('Passenger 6', 191, 'Earth', 'Uranus')
    p13 = Passenger('Passenger 13', 134, 'Mercury', 'Uranus')
    p10 = Passenger('Passenger 10', 19, 'Earth', 'Planet X')
    p9 = Passenger('Passenger 9', 162, 'Earth', 'Mercury')
    p3 = Passenger('Passenger 3', 7, 'Earth', 'Mercury')
    p5 = Passenger('Passenger 5', 82, 'Mercury', 'Planet X')
    p11 = Passenger('Passenger 11', 124, 'Uranus', 'Planet X')
    p4 = Passenger('Passenger 4', 154, 'Mercury', 'Planet X')
    p8 = Passenger('Passenger 8', 186, 'Uranus', 'Planet X')
    p14 = Passenger('Passenger 14', 62, 'Planet X', 'Uranus')
    p7 = Passenger('Passenger 7', 131, 'Mercury', 'Planet X')
    p2 = Passenger('Passenger 2', 125, 'Earth', 'Planet X')
    p12 = Passenger('Passenger 12', 108, 'Uranus', 'Planet X')
    passengers = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14]
    #
    # dmap = DistanceMap()
    # dmap.add_distance("Earth", "Uranus", 3)
    # dmap.add_distance("Earth", "Jupiter", 1)
    # dmap.add_distance("Jupiter", "Earth", 3)
    # dmap.add_distance("Earth", "Saturn", 4)
    # dmap.add_distance("Earth", "Venus", 4)
    # dmap.add_distance("Earth", "Neptune")- Neptune: 1
    # dmap.add_distance("Neptune", "Earth")e - Earth: 1
    # dmap.add_distance("Earth", "Pluto")- Pluto: 1
    # dmap.add_distance("Earth", "Mercury")- Mercury: 1
    # dmap.add_distance("Mercury", "Earth")y - Earth: 1
    # dmap.add_distance("Earth", "Mars")- Mars: 3
    # dmap.add_distance("Mars", "Earth") Earth: 4
    # dmap.add_distance("Earth", "Planet X")- Planet X: 3
    # dmap.add_distance("Planet X", "Earth") X - Earth: 2
    # dmap.add_distance("Uranus", "Jupiter") - Jupiter: 3
    # dmap.add_distance("Uranus", "Saturn") - Saturn: 3
    # dmap.add_distance("Uranus", "Venus") - Venus: 1
    # dmap.add_distance("Uranus", "Neptune") - Neptune: 2
    # dmap.add_distance("Uranus", "Pluto") - Pluto: 4
    # dmap.add_distance("Pluto", "Uranus")- Uranus: 1
    # dmap.add_distance("Uranus", "Mercury") - Mercury: 2
    # dmap.add_distance("Uranus", "Mars") - Mars: 1
    # dmap.add_distance("Mars", "Uranus") Uranus: 3
    # dmap.add_distance("Uranus", "Planet X") - Planet X: 2
    # dmap.add_distance("Planet X", "Uranus") X - Uranus: 3
    # dmap.add_distance("Jupiter", "Saturn")r - Saturn: 3
    # dmap.add_distance("Saturn", "Jupiter") - Jupiter: 4
    # dmap.add_distance("Jupiter", "Venus")r - Venus: 4
    # dmap.add_distance("Venus", "Jupiter")- Jupiter: 3
    # dmap.add_distance("Jupiter", "Neptune")r - Neptune: 2
    # dmap.add_distance("Jupiter", "Pluto")r - Pluto: 2
    # dmap.add_distance("Pluto", "Jupiter")- Jupiter: 1
    # dmap.add_distance("Jupiter", "Mercury")r - Mercury: 4
    # dmap.add_distance("Mercury", "Jupiter")y - Jupiter: 1
    # dmap.add_distance("Jupiter", "Mars")r - Mars: 3
    # dmap.add_distance("Jupiter", "Planet X")r - Planet X: 2
    # dmap.add_distance("Planet X", "Jupiter") X - Jupiter: 3
    # dmap.add_distance("Saturn", "Venus") - Venus: 3
    # dmap.add_distance("Venus", "Saturn", 1)
    # dmap.add_distance("Saturn", "Neptune", 4)
    # dmap.add_distance("Neptune", "Saturn", 3)
    # dmap.add_distance("Saturn", "Pluto", 3)
    # dmap.add_distance("Saturn", "Mercury", 4)
    # dmap.add_distance("Saturn", "Mars", 1)
    # dmap.add_distance("Saturn", "Planet X", 3)
    # dmap.add_distance("Venus", "Neptune", 3)
    # dmap.add_distance("Venus", "Pluto", 1)
    # dmap.add_distance("Venus", "Mercury", 2)
    # dmap.add_distance("Mercury", "Venus", 2)
    # dmap.add_distance("Venus", "Mars", 4)
    # dmap.add_distance("Mars") Venus: 4
    # dmap.add_distance("Venus")- Planet X: 2
    # dmap.add_distance("Planet") X - Venus: 3
    # dmap.add_distance("Neptune")e - Pluto: 3
    # dmap.add_distance("Pluto")- Neptune: 1
    # dmap.add_distance("Neptune")e - Mercury: 4
    # dmap.add_distance("Neptune")e - Mars: 1
    # dmap.add_distance("Mars") Neptune: 1
    # dmap.add_distance("Neptune")e - Planet X: 2
    # dmap.add_distance("Pluto")- Mercury: 1
    # dmap.add_distance("Pluto")- Mars: 1
    # dmap.add_distance("Mars") Pluto: 4
    # dmap.add_distance("Pluto")- Planet X: 3
    # dmap.add_distance("Mercury")y - Mars: 1
    # dmap.add_distance("Mercur")y - Planet X: 3
    # dmap.add_distance("Mars") Planet X: 2
    # dmap.add_distance("Planet X") X - Mars: 1

# SpaceBikes:
#     SpaceBike(0, 'Atom Bike', 3, 3.81, 0.48) with Passengers:
#           Passenger('Passenger 1', 96, 'Earth', 'Mercury')
#         Passenger('Passenger 6', 191, 'Earth', 'Uranus')
#         Passenger('Passenger 13', 134, 'Mercury', 'Uranus')
#     SpaceBike(1, 'Nova Bike', 20, 7.54, 0.9) with Passengers:
#           Passenger('Passenger 10', 19, 'Earth', 'Planet X')
#         Passenger('Passenger 9', 162, 'Earth', 'Mercury')
#         Passenger('Passenger 3', 7, 'Earth', 'Mercury')
#
# Unboarded passengers:
#     Passenger('Passenger 5', 82, 'Mercury', 'Planet X')
#     Passenger('Passenger 11', 124, 'Uranus', 'Planet X')
#     Passenger('Passenger 4', 154, 'Mercury', 'Planet X')
#     Passenger('Passenger 8', 186, 'Uranus', 'Planet X')
#     Passenger('Passenger 14', 62, 'Planet X', 'Uranus')
#     Passenger('Passenger 7', 131, 'Mercury', 'Planet X')
#     Passenger('Passenger 2', 125, 'Earth', 'Planet X')
#     Passenger('Passenger 12', 108, 'Uranus', 'Planet X')
# DistanceMap with entries:
#       Earth - Uranus: 3
#     Earth - Jupiter: 1
#     Jupiter - Earth: 3
#     Earth - Saturn: 4
#     Earth - Venus: 4
#     Earth - Neptune: 1
#     Neptune - Earth: 1
#     Earth - Pluto: 1
#     Earth - Mercury: 1
#     Mercury - Earth: 1
#     Earth - Mars: 3
#     Mars - Earth: 4
#     Earth - Planet X: 3
#     Planet X - Earth: 2
#     Uranus - Jupiter: 3
#     Uranus - Saturn: 3
#     Uranus - Venus: 1
#     Uranus - Neptune: 2
#     Uranus - Pluto: 4
#     Pluto - Uranus: 1
#     Uranus - Mercury: 2
#     Uranus - Mars: 1
#     Mars - Uranus: 3
#     Uranus - Planet X: 2
#     Planet X - Uranus: 3
#     Jupiter - Saturn: 3
#     Saturn - Jupiter: 4
#     Jupiter - Venus: 4
#     Venus - Jupiter: 3
#     Jupiter - Neptune: 2
#     Jupiter - Pluto: 2
#     Pluto - Jupiter: 1
#     Jupiter - Mercury: 4
#     Mercury - Jupiter: 1
#     Jupiter - Mars: 3
#     Jupiter - Planet X: 2
#     Planet X - Jupiter: 3
#     Saturn - Venus: 3
#     Venus - Saturn: 1
#     Saturn - Neptune: 4
#     Neptune - Saturn: 3
#     Saturn - Pluto: 3
#     Saturn - Mercury: 4
#     Saturn - Mars: 1
#     Saturn - Planet X: 3
#     Venus - Neptune: 3
#     Venus - Pluto: 1
#     Venus - Mercury: 2
#     Mercury - Venus: 2
#     Venus - Mars: 4
#     Mars - Venus: 4
#     Venus - Planet X: 2
#     Planet X - Venus: 3
#     Neptune - Pluto: 3
#     Pluto - Neptune: 1
#     Neptune - Mercury: 4
#     Neptune - Mars: 1
#     Mars - Neptune: 1
#     Neptune - Planet X: 2
#     Pluto - Mercury: 1
#     Pluto - Mars: 1
#     Mars - Pluto: 4
#     Pluto - Planet X: 3
#     Mercury - Mars: 1
#     Mercury - Planet X: 3
#     Mars - Planet X: 2
#     Planet X - Mars: 1
