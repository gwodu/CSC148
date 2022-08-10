import random
from typing import List, Dict, Callable, Any, Tuple, Optional

from a2_space_bikes import Passenger, SpaceBike, SpaceFleet
from a2_container import PriorityQueue
from typing import Dict, List, Union, Optional
from a2_fleet_scheduler import BogoScheduler, GreedyScheduler, FleetScheduler
from a2_space_bikes import SpaceBike, SpaceFleet, Passenger
from a2_distance_map import DistanceMap
from a2_command_central import load_fleet_data, load_galaxy_data, load_passenger_data

f_name = "/Users/g.l.wodu/Desktop/CSC148/csc148/assignments/a2/release/data/testing/space_fleet_data_larger.txt"
data = load_fleet_data(f_name)
print(data.num_space_bikes())
print(data.num_nonempty_bikes())
for bike in data.bikes:
    print(bike.bike_type)
