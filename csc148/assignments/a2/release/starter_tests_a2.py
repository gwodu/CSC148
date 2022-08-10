from a2_space_bikes import SpaceFleet, SpaceBike, Passenger
from a2_container import PriorityQueue, _QueueNode
from a2_command_central import CommandCentral
from a2_distance_map import DistanceMap
from a2_fleet_scheduler import BogoScheduler, GreedyScheduler, _space_bike_priority, _sort_bikes_by_capacity, _sb_priority_capacity, _sb_priority_fuel, _return_bike_enroute_poss_bikes
import tempfile


def test_distance_map():
    dmap = DistanceMap()
    dmap.add_distance("Earth", "Mars", 0.1)
    dmap.add_distance("Earth", "Venus", 0.2)
    dmap.add_distance("Mars", "Venus", 0.5)

    assert dmap.distance("Earth", "Mars") == 0.1
    assert dmap.distance("Mars", "Earth") == 0.1

    assert dmap.distance("Earth", "Venus") == 0.2
    assert dmap.distance("Venus", "Earth") == 0.2

    assert dmap.distance("Venus", "Mars") == 0.5
    assert dmap.distance("Mars", "Venus") == 0.5


def test_space_bikes():
    sf = SpaceFleet()
    b1 = SpaceBike(100, "Nova Bike", 20, 8.0, 0.5)

    sf.add_space_bike(b1)

    dmap = DistanceMap()
    dmap.add_distance("Earth", "Mars", 0.1)
    dmap.add_distance("Earth", "Venus", 0.2)
    dmap.add_distance("Mars", "Venus", 0.5)

    # --------------------------------------------------
    #   Board a single passenger, starting in bike route
    # --------------------------------------------------

    p1 = Passenger("MaryAnn Jacobs", 1.0, "Earth", "Mars")
    assert b1.board(p1, dmap)
    assert sf.passenger_placements() == {
        100: ["MaryAnn Jacobs"]
    }
    assert sf.total_fare_collected() == 1.0
    assert sf.total_distance_travelled(dmap) == 0.1
    assert sf.vacant_seats() == 19

    # --------------------------------------------------
    #   Board a second passenger, starting in bike route
    # --------------------------------------------------
    p2 = Passenger("Richard LeFeuille", 1.0, "Earth", "Mars")
    assert b1.board(p2, dmap)
    assert sf.passenger_placements() == {
        100: ["MaryAnn Jacobs", "Richard LeFeuille"]
    }
    assert sf.total_fare_collected() == 2.0
    assert sf.total_distance_travelled(dmap) == 0.1
    assert sf.vacant_seats() == 18

    # --------------------------------------------------
    #   Try to board a third passenger, starting not in
    #   bike route
    # --------------------------------------------------
    p3 = Passenger("Howl Jenkins", 1.0, "Venus", "Mars")
    assert not b1.board(p3, dmap)
    assert sf.passenger_placements() == {
        100: ["MaryAnn Jacobs", "Richard LeFeuille"]
    }
    assert sf.total_fare_collected() == 2.0
    assert sf.total_distance_travelled(dmap) == 0.1
    assert sf.vacant_seats() == 18


def test_ultimate_board_test():
    sf = SpaceFleet()
    b1 = SpaceBike(100, "Nova Bike", 20, 8.0, 0.5)
    assert b1.travel_chart == [("Earth",)]

    sf.add_space_bike(b1)

    dmap = DistanceMap()
    dmap.add_distance("Earth", "Mars", 0.1)
    dmap.add_distance("Earth", "Venus", 0.2)
    dmap.add_distance("Mars", "Venus", 0.5)
    dmap.add_distance("Mars", "Jupiter", 0.5)
    dmap.add_distance("Mars", "Earth", 50)

    p0 = Passenger("Jeffery", 1.0, "Mars", "Venus")
    p1 = Passenger("MaryAnn Jacobs", 1.0, "Earth", "Mars")
    p2 = Passenger("Jefferson Pak", 1.0, "Earth", "Mars")
    p3 = Passenger("Gabriel Aderantin", 1.0, "Venus", "Mars")
    p4 = Passenger("Michelle Spatswick", 1.0, "Earth", "Jupiter")
    p5 = Passenger("Wuami Yause", 1.0, "Jupiter", "Mars")
    p6 = Passenger("Independence John", 1.0, "Mars", "Earth")

    assert not b1.board(p0, dmap)
    assert b1.travel_chart == [("Earth",)]
    assert b1.board(p1, dmap)
    assert b1.travel_chart == [("Earth","Mars")]
    assert b1.board(p2, dmap)
    assert b1.travel_chart == [("Earth","Mars")]
    assert not b1.board(p3, dmap)
    assert b1.travel_chart == [("Earth","Mars")]
    assert b1.board(p4, dmap)
    assert b1.travel_chart == [("Earth","Mars"), ("Mars", "Jupiter")]
    assert b1.board(p5, dmap)
    assert b1.travel_chart == [("Earth","Mars"), ("Mars", "Jupiter"),
                               ("Jupiter", "Mars")]
    assert not b1.board(p6, dmap) #not enough fuel

    assert b1.travel_chart == [("Earth", "Mars"), ("Mars", "Jupiter"), (
        "Jupiter", "Mars")]
    assert b1.passenger_list == [p1, p2, p4, p5]
    assert b1._route_distance(dmap) == 1.1
    assert b1.fare_collected == 4.0
    assert b1.fuel_level == b1.max_fuel_capacity

def test_priority_queue():
    pq = PriorityQueue(int.__lt__)
    assert pq.is_empty()

    pq.add(1000)
    assert str(pq) == '1000'
    pq.add(10)
    assert str(pq) == '10 -> 1000'
    pq.add(0)
    assert str(pq) == '0 -> 10 -> 1000'
    pq.add(200)
    assert str(pq) == '0 -> 10 -> 200 -> 1000'
    pq.add(50)
    assert str(pq) == '0 -> 10 -> 50 -> 200 -> 1000'
    pq.add(60)
    assert str(pq) == '0 -> 10 -> 50 -> 60 -> 200 -> 1000'
    pq.add(-20)
    assert str(pq) == '-20 -> 0 -> 10 -> 50 -> 60 -> 200 -> 1000'
    pq.add(2000)
    assert str(pq) == '-20 -> 0 -> 10 -> 50 -> 60 -> 200 -> 1000 -> 2000'

    assert isinstance(pq._first, _QueueNode)
    assert not pq.is_empty()

    # val1 = pq.remove()
    # val2 = pq.remove()
    # val3 = pq.remove()
    # val4 = pq.remove()
    # val5 = pq.remove()
    # val6 = pq.remove()
    #
    # assert val1 == 0
    # assert val2 == 10
    # assert val3 == 50
    # assert val4 == 60
    # assert val5 == 200
    # assert val6 == 1000

def test_space_bike_priority():
    dmap = DistanceMap()
    dmap.add_distance("Earth", "Mars", 1.0)
    dmap.add_distance("Earth", "Mercury", 1.0)
    dmap.add_distance("Earth", "Fr18", 1.0)
    dmap.add_distance("Earth", "Juniper", 1.0)
    dmap.add_distance("Earth", "Neptune", 1.0)
    dmap.add_distance("Mercury", "Mars", 1.0)
    dmap.add_distance("Mars", "Jupiter", 1.0)
    dmap.add_distance("Jupiter", "Neptune", 1.0)
    dmap.add_distance("Jupiter", "Fr18", 1.0)
    dmap.add_distance("Fr18", "Neptune", 1.0)
    dmap.add_distance("Fr18", "Mars", 1.0)
    dmap.add_distance("Mars", "Neptune", 1.0)
    dmap.add_distance("Molestus", "Mars", 1.0)
    dmap.add_distance("Mercury", "Jupiter", 1.0)
    dmap.add_distance("Neptune", "Juniper", 1.0)
    dmap.add_distance("Mars", "Juniper", 1.0)

    p_1 = Passenger("Juniper,,", 1.0, "Earth", "Earth")
    p0 = Passenger("Juniper,", 1.0, "Earth", "Juniper")
    p1 = Passenger("Francis", 1.0, "Earth", "Mars")
    p1.give_distance(dmap)
    p2 = Passenger("Patricia,", 1.0, "Molestus", "Mars")
    p2.give_distance(dmap)
    p3 = Passenger("P4treeshia", 1.0, "Mercury", "Jupiter")
    p3.give_distance(dmap)
    p4 = Passenger("Irron", 1.0, "Earth", "Neptune")
    p4.give_distance(dmap)

    sb_1 = SpaceBike(9999, "Nova Bike", 0, 8.0, 0.5)

    sb0 = SpaceBike(10000, "Nova Bike", 1, 8.0, 0.5)

    sb1 = SpaceBike(10001, "Nova Bike", 10, 8.0, 0.5)
    sb1.travel_chart = [("Earth", "Mars")]

    sb2 = SpaceBike(10002, "Nova Bike", 8, 8.0, 0.5)
    sb2.travel_chart = [("Earth", "Mercury"), ("Mercury", "Mars")]

    sb3 = SpaceBike(10003, "Nova Bike", 6, 8.0, 0.5)
    sb3.travel_chart = [("Earth", "Mercury"), ("Mercury", "Mars"), ("Mars", "Jupiter"),
        ("Jupiter", "Neptune")]

    sb4 = SpaceBike(10004, "Nova Bike", 4, 8.0, 0.5)
    sb4.travel_chart = [("Earth", "Mercury"), ("Mercury", "Mars"), ("Mars", "Jupiter"),
        ("Jupiter", "Fr18"), ("Fr18", "Neptune")]

    sb5 = SpaceBike(10005, "Nova Bike", 2, 8.0, 0.5)
    sb5.travel_chart = [("Earth", "Fr18"), ("Fr18", "Mars"), ("Mars", "Neptune")]

    space_bikes = [sb_1, sb0, sb1, sb2, sb3, sb4, sb5]

    assert _space_bike_priority(p0,space_bikes, dmap).id == sb0.id
    assert _space_bike_priority(p1,[sb1], dmap).id == sb1.id
    assert _space_bike_priority(p2,[sb0], dmap) == None
    assert _space_bike_priority(p1,space_bikes, dmap).id == sb5.id
    assert _space_bike_priority(p2,space_bikes, dmap) == None
    assert _space_bike_priority(p3,space_bikes, dmap).id == sb4.id
    assert _space_bike_priority(p4,space_bikes, dmap).id == sb5.id
    assert _space_bike_priority(p_1, space_bikes, dmap).id == sb0.id

def test_space_bike_priority_specifications():
    dmap = DistanceMap()
    dmap.add_distance("Earth", "Mars", 1.0)
    dmap.add_distance("Earth", "Mercury", 1.0)
    dmap.add_distance("Earth", "Fr18", 1.0)
    dmap.add_distance("Earth", "Juniper", 1.0)
    dmap.add_distance("Earth", "Neptune", 1.0)
    dmap.add_distance("Mercury", "Mars", 1.0)
    dmap.add_distance("Mars", "Jupiter", 1.0)
    dmap.add_distance("Jupiter", "Neptune", 1.5)
    dmap.add_distance("Jupiter", "Fr18", 1.0)
    dmap.add_distance("Fr18", "Neptune", 1.0)
    dmap.add_distance("Fr18", "Mars", 1.0)
    dmap.add_distance("Mars", "Neptune", 1.0)
    dmap.add_distance("Molestus", "Mars", 1.0)
    dmap.add_distance("Mercury", "Jupiter", 1.0)
    dmap.add_distance("Neptune", "Juniper", 1.0)
    dmap.add_distance("Mars", "Juniper", 1.0)
    dmap.add_distance("Mars", "Molestus", 3.0)
    dmap.add_distance("Neptune", "Molestus", 2.0)


    p0 = Passenger("Juniper,", 1.0, "Earth", "Juniper")
    p1 = Passenger("Francis", 1.0, "Earth", "Mars")
    p1.give_distance(dmap)
    p2 = Passenger("Patricia,", 1.0, "Mars", "Molestus")
    p2.give_distance(dmap)
    p3 = Passenger("P4treeshia", 1.0, "Mercury", "Jupiter")
    p3.give_distance(dmap)
    p4 = Passenger("Irron", 1.0, "Earth", "Neptune")
    p4.give_distance(dmap)

    sb0 = SpaceBike(10000, "Nova Bike", 1, 8.0, 0.5)

    sb1 = SpaceBike(10001, "Nova Bike", 10, 8.0, 0.5)
    sb1.travel_chart = [("Earth", "Mars")]

    sb2 = SpaceBike(10002, "Nova Bike", 8, 8.0, 0.5)
    sb2.travel_chart = [("Earth", "Mercury"), ("Mercury", "Mars")]

    sb3 = SpaceBike(10003, "Nova Bike", 6, 8.0, 0.5)
    sb3.travel_chart = [("Earth", "Mercury"), ("Mercury", "Mars"), ("Mars", "Jupiter"),
                        ("Jupiter", "Neptune")]

    sb4 = SpaceBike(10004, "Nova Bike", 4, 8.0, 0.5)
    sb4.travel_chart = [("Earth", "Mercury"), ("Mercury", "Mars"), ("Mars", "Jupiter"),
                        ("Jupiter", "Fr18"), ("Fr18", "Neptune")]

    sb5 = SpaceBike(10005, "Nova Bike", 2, 8.0, 0.5)
    sb5.travel_chart = [("Earth", "Fr18"), ("Fr18", "Mars"), ("Mars", "Neptune")]

    space_bikes = [sb0, sb1, sb2, sb3, sb4, sb5]

    assert _space_bike_priority(p3, space_bikes, dmap).id == sb4.id
    assert _space_bike_priority(p2, space_bikes, dmap).id == sb5.id

def test_space_bike_priority_id():
    dmap = DistanceMap()
    dmap.add_distance("Earth", "Mars", 1.0)
    dmap.add_distance("Earth", "Mercury", 1.0)
    dmap.add_distance("Earth", "Fr18", 1.0)
    dmap.add_distance("Earth", "Juniper", 1.0)
    dmap.add_distance("Earth", "J4l4pinyos", 230.0)
    dmap.add_distance("Earth", "Neptune", 1.0)
    dmap.add_distance("Mercury", "Mars", 1.0)
    dmap.add_distance("Mars", "Jupiter", 1.0)
    dmap.add_distance("Mars", "J4l4pinyos", 230.0)
    dmap.add_distance("Jupiter", "Neptune", 1.5)
    dmap.add_distance("Jupiter", "Fr18", 1.0)
    dmap.add_distance("Fr18", "Neptune", 1.0)
    dmap.add_distance("Fr18", "Mars", 1.0)
    dmap.add_distance("Mars", "Neptune", 1.0)
    dmap.add_distance("Molestus", "Mars", 1.0)
    dmap.add_distance("Mercury", "Jupiter", 1.0)
    dmap.add_distance("Neptune", "Juniper", 1.0)
    dmap.add_distance("Mars", "Juniper", 1.0)
    dmap.add_distance("Mars", "Molestus", 3.0)
    dmap.add_distance("Neptune", "Molestus", 2.0)
    dmap.add_distance("Neptune", "J4l4pinyos", 230.0)


    p0 = Passenger("Juniper,", 1.0, "Earth", "Juniper")
    p1 = Passenger("Francis", 1.0, "Earth", "Mars")
    p1.give_distance(dmap)
    p2 = Passenger("Patricia,", 1.0, "Mars", "Molestus")
    p2.give_distance(dmap)
    p3 = Passenger("P4treeshia", 1.0, "Mercury", "Jupiter")
    p3.give_distance(dmap)
    p4 = Passenger("Irron", 1.0, "Earth", "J4l4pinyos")
    p4.give_distance(dmap)

    sb0 = SpaceBike(10000, "Nova Bike", 1, 8.0, 0.5)

    sb1 = SpaceBike(10001, "Nova Bike", 10, 8.0, 0.5)
    sb1.travel_chart = [("Earth", "Mars")]

    sb2 = SpaceBike(10002, "Nova Bike", 8, 8.0, 0.1)
    sb2.travel_chart = [("Earth", "Mercury"), ("Mercury", "Mars")]

    sb3 = SpaceBike(10003, "Nova Bike", 6, 8.0, 0.2)
    sb3.travel_chart = [("Earth", "Mercury"), ("Mercury", "Mars"), ("Mars", "Jupiter"),
                        ("Jupiter", "Neptune")]

    sb4 = SpaceBike(10004, "Nova Bike", 2, 8.0, 0.4)
    sb4.travel_chart = [("Earth", "Mercury"), ("Mercury", "Mars"), ("Mars", "Jupiter"),
                        ("Jupiter", "Fr18"), ("Fr18", "Neptune")]

    sb5 = SpaceBike(10005, "Nova Bike", 2, 8.0, 0.1)
    sb5.travel_chart = [("Earth", "Fr18"), ("Fr18", "Mars"), ("Mars", "Neptune")]

    space_bikes = [sb0, sb1, sb2, sb3, sb4, sb5]

    assert _space_bike_priority(p0, space_bikes, dmap).id == sb5.id  # fuel consumption tie with sb2 and sb5, settled by capacity
    assert _space_bike_priority(p2, space_bikes, dmap).id == sb5.id
    assert _space_bike_priority(p4, space_bikes, dmap) == None

def test_greedyscheduler_schedule():
    dmap = DistanceMap()
    dmap.add_distance("Earth", "Mars", 1.0)
    dmap.add_distance("Earth", "Mercury", 1.0)
    dmap.add_distance("Earth", "Fr18", 1.0)
    dmap.add_distance("Earth", "Juniper", 1.0)
    dmap.add_distance("Earth", "J4l4pinyos", 230.0)
    dmap.add_distance("Earth", "Neptune", 1.0)
    dmap.add_distance("Mercury", "Mars", 1.0)
    dmap.add_distance("Mars", "Jupiter", 1.0)
    dmap.add_distance("Mars", "J4l4pinyos", 230.0)
    dmap.add_distance("Jupiter", "Neptune", 1.5)
    dmap.add_distance("Jupiter", "Fr18", 1.0)
    dmap.add_distance("Fr18", "Neptune", 1.0)
    dmap.add_distance("Fr18", "Mars", 1.0)
    dmap.add_distance("Mars", "Neptune", 1.0)
    dmap.add_distance("Molestus", "Mars", 1.0)
    dmap.add_distance("Mercury", "Jupiter", 1.0)
    dmap.add_distance("Neptune", "Juniper", 1.0)
    dmap.add_distance("Mars", "Juniper", 1.0)
    dmap.add_distance("Mars", "Molestus", 3.0)
    dmap.add_distance("Neptune", "Molestus", 2.0)
    dmap.add_distance("Neptune", "J4l4pinyos", 230.0)
    dmap.add_distance("Jupiter", "Molestus", 1.0)
    dmap.add_distance("Juniper", "J4l4pinyos", 1.0)
    dmap.add_distance("Jupiter", "J4l4pinyos", 1.0)
    dmap.add_distance("Molestus", "J4l4pinyos", 230.0)
    dmap.add_distance("Crowayshi,a", "Mercury", 1.0)

    p_1 = Passenger("Juniper-1,", 1.0, "Earth", "Earth")
    p0 = Passenger("Juniper,", 1.0, "Earth", "Juniper")
    p1 = Passenger("Francis", 1.0, "Earth", "Mars")
    p2 = Passenger("Patricia,", 1.0, "Mars", "Molestus")
    p3 = Passenger("P4treeshia", 1.0, "Mercury", "Jupiter")
    p4 = Passenger("Irron", 1.0, "Earth", "J4l4pinyos")
    p5 = Passenger("Irron,,", 1.0, "Crowayshi,a", "Mercury")

    sb0 = SpaceBike(10000, "Nova Bike", 1, 8.0, 0.5)

    sb1 = SpaceBike(10001, "Nova Bike", 10, 8.0, 0.5)
    sb1.travel_chart = [("Earth", "Mars")]

    sb2 = SpaceBike(10002, "Nova Bike", 8, 8.0, 0.5)
    sb2.travel_chart = [("Earth", "Mercury"), ("Mercury", "Mars")]

    sb3 = SpaceBike(10003, "Nova Bike", 6, 8.0, 0.5)
    sb3.travel_chart = [("Earth", "Mercury"), ("Mercury", "Mars"), ("Mars", "Jupiter"),
                        ("Jupiter", "Neptune")]

    sb4 = SpaceBike(10004, "Nova Bike", 2, 8.0, 0.5)
    sb4.travel_chart = [("Earth", "Mercury"), ("Mercury", "Mars"), ("Mars", "Jupiter"),
                        ("Jupiter", "Fr18"), ("Fr18", "Neptune")]

    sb5 = SpaceBike(10005, "Nova Bike", 2, 8.0, 0.5)
    sb5.travel_chart = [("Earth", "Fr18"), ("Fr18", "Mars"), ("Mars", "Neptune")]

    space_bikes = [sb0, sb1, sb2, sb3, sb4, sb5]
    passengers = [p_1, p0, p1, p2, p3, p4, p5]

    gs = GreedyScheduler(dmap, "fare_per_dist")
    board_dict = gs.schedule(passengers, space_bikes, verbosity= 1)
    assert p4 not in board_dict[True]
    assert p0 in board_dict[True]
    assert p1 in board_dict[True]
    assert p2 in board_dict[True]
    assert p3 in board_dict[True]
    assert p5 not in board_dict[True]
    assert p_1 in board_dict[True]
    # assert sb0.travel_chart == "Eggs"
    # assert sb0.curr_capacity == 0
    # assert sb5.curr_capacity == 2
    # assert sb5.passenger_name_list == "eggs"

def _create_bogo_cc() -> CommandCentral:
    config = {
        "scheduler_type": "bogo",
        "verbosity": 0,
        "passenger_priority": "fare_per_dist",
        "passenger_fname": "./data/testing/passengers_off_peak.txt",
        "galaxy_fname": "./data/galaxy_data.txt",
        "fleet_fname": "./data/testing/space_fleet_data.txt"
    }

    return CommandCentral(config)


def _create_greedy_cc() -> CommandCentral:
    config = {
        "scheduler_type": "greedy",
        "verbosity": 1,
        "passenger_priority": "fare_bid",
        "passenger_fname": "./data/testing/passengers_off_peak.txt",
        "galaxy_fname": "./data/galaxy_data.txt",
        "fleet_fname": "./data/testing/space_fleet_data.txt"
    }

    return CommandCentral(config)


def test_command_central_attributes():
    cc1 = _create_bogo_cc()

    assert isinstance(cc1.scheduler, BogoScheduler)
    assert cc1.fleet.num_space_bikes() == 33
    assert cc1.verbosity == 0
    assert isinstance(cc1.dmap, DistanceMap)
    assert len(cc1.passengers) == 35

    cc2 = _create_greedy_cc()

    assert isinstance(cc2.scheduler, GreedyScheduler)
    assert cc2.fleet.num_space_bikes() == 33
    assert cc2.verbosity == 1
    assert isinstance(cc2.dmap, DistanceMap)
    assert len(cc2.passengers) == 35


def test_fleet_bogo_scheduler():
    fleet_str = """\
Nova Bike
ID_100\t20\t8.0\t0.5
    """

    tmp_fleet_file = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
    tmp_fleet_file.write(fleet_str)

    passenger_str = """\
MaryAnn Jacobs
BID: 1.0\tSOURCE: Earth\tDEST: Mars
Canus Rex
BID: 0.5\tSOURCE: Earth\tDEST: Mars
Riley Adams
 BID: 2.0\tSOURCE: Venus\tDEST: Earth
    """

    tmp_passenger_file = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
    tmp_passenger_file.write(passenger_str)

    galaxy_str = """\
Earth\tMars\t0.1
Earth\tVenus\t0.2
Mars\tVenus\t0.5
    """

    tmp_galaxy_file = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
    tmp_galaxy_file.write(galaxy_str)

    config = {
        "scheduler_type": "bogo",
        "verbosity": 0,
        "passenger_fname": f"{tmp_passenger_file.name}",
        "galaxy_fname": f"{tmp_galaxy_file.name}",
        "fleet_fname": f"{tmp_fleet_file.name}"
    }

    tmp_galaxy_file.close()
    tmp_fleet_file.close()
    tmp_passenger_file.close()

    cc = CommandCentral(config)

    # run the scheduler
    cc.run(report=False)

    passenger_placements = cc.fleet.passenger_placements()

    assert "MaryAnn Jacobs" in passenger_placements[100]
    assert "Canus Rex" in passenger_placements[100]
    assert "Riley Adams" not in passenger_placements[100]


def test_fleet_greedy_scheduler():
    fleet_str = """\
    Nova Bike
    ID_100\t20\t8.0\t0.5
        """

    tmp_fleet_file = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
    tmp_fleet_file.write(fleet_str)

    passenger_str = """\
    MaryAnn Jacobs
    BID: 1.0\tSOURCE: Earth\tDEST: Mars
    Canus Rex
    BID: 0.5\tSOURCE: Earth\tDEST: Mars
    Riley Adams
     BID: 2.0\tSOURCE: Venus\tDEST: Earth
        """

    tmp_passenger_file = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
    tmp_passenger_file.write(passenger_str)

    galaxy_str = """\
    Earth\tMars\t0.1
    Earth\tVenus\t0.2
    Mars\tVenus\t0.5
        """

    tmp_galaxy_file = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
    tmp_galaxy_file.write(galaxy_str)

    config = {
        "scheduler_type": "greedy",
        "verbosity": 0,
        "passenger_priority": "fare_bid",
        "passenger_fname": f"{tmp_passenger_file.name}",
        "galaxy_fname": f"{tmp_galaxy_file.name}",
        "fleet_fname": f"{tmp_fleet_file.name}"
    }

    tmp_galaxy_file.close()
    tmp_fleet_file.close()
    tmp_passenger_file.close()

    cc = CommandCentral(config)

    # run the scheduler
    cc.run(report=False)

    passenger_placements = cc.fleet.passenger_placements()
    assert passenger_placements[100] == ["MaryAnn Jacobs", "Canus Rex"]

def test_fleet_greedy_scheduler_handout():
    fleet_str = """\
    Atom Bike
    ID_1\t2\t4.0\t0.5
    Atom Bike
    ID_2\t4\t4.0\t0.5
    Nova Bike
    ID_3\t20\t8.0\t1.0
        """

    tmp_fleet_file = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
    tmp_fleet_file.write(fleet_str)

    passenger_str = """\
    Laura Engelman
    BID: 2.5\tSOURCE: Earth\tDEST: Venus
    Jonathan McMyers
    BID: 1.5\tSOURCE: Sun\tDEST: Venus
    MaryAnn Jacobs
    BID: 1.0\tSOURCE: Earth\tDEST: Mars
    Robert Robarts
    BID: 0.5\tSOURCE: Venus\tDEST: Sun
    Lily Jenkins
    BID: 0.2\tSOURCE: Venus\tDEST: Sun
    Melanie Kim
     BID: 0.1\tSOURCE: Earth\tDEST: Venus
        """

    tmp_passenger_file = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
    tmp_passenger_file.write(passenger_str)

    galaxy_str = """\
    Earth\tVenus\t4.5
    Sun\tVenus\t1.0
    Earth\tMars\t2.0
    Venus\tMars\t4.0
        """

    tmp_galaxy_file = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
    tmp_galaxy_file.write(galaxy_str)

    config = {
        "scheduler_type": "greedy",
        "verbosity": 10,
        "passenger_priority": "fare_bid",
        "passenger_fname": f"{tmp_passenger_file.name}",
        "galaxy_fname": f"{tmp_galaxy_file.name}",
        "fleet_fname": f"{tmp_fleet_file.name}"
    }

    tmp_galaxy_file.close()
    tmp_fleet_file.close()
    tmp_passenger_file.close()

    cc = CommandCentral(config)

    # run the scheduler
    cc.run(report=False)

    passenger_placements = cc.fleet.passenger_placements()
    assert passenger_placements[1] == ["Laura Engelman", "Robert Robarts"]
    assert passenger_placements[2] == ["MaryAnn Jacobs", "Melanie Kim", "Lily Jenkins", "Jonathan McMyers"]

def test_sort_bike_by_capacity():
    sb1 = SpaceBike(198761, 'Nova Bike', 20, 8.0, 0.5)
    sb2 = SpaceBike(198762, 'Nova Bike', 1, 8.0, 0.5)
    sb3 = SpaceBike(198763, 'Nova Bike', 0, 8.0, 0.5)
    sb4 = SpaceBike(198764, 'Nova Bike', 10, 8.0, 0.5)
    sb5 = SpaceBike(198765, 'Nova Bike', 20, 8.0, 0.5)
    sb6 = SpaceBike(197567, 'Nova Bike', 0, 8.0, 0.5)
    sb7 = SpaceBike(198732, 'Nova Bike', 1, 8.0, 0.5)
    sb_list = [sb1, sb2, sb3, sb4, sb5, sb6, sb7]
    sorted_list = _sort_bikes_by_capacity(sb_list)
    assert sorted_list[0] == sb3
    assert sorted_list[1] == sb6
    assert sorted_list[2] == sb2
    assert sorted_list[3] == sb7
    assert sorted_list[4] == sb4
    assert sorted_list[5] == sb1
    assert sorted_list[6] == sb5

def test_sb_priority_capacity():
    sb1 = SpaceBike(198761, 'Nova Bike', 20, 8.0, 0.5)
    sb2 = SpaceBike(198762, 'Nova Bike', 1, 8.0, 0.5)
    sb3 = SpaceBike(198763, 'Nova Bike', 0, 8.0, 0.5)
    sb4 = SpaceBike(198764, 'Nova Bike', 10, 8.0, 0.5)
    sb5 = SpaceBike(198765, 'Nova Bike', 20, 8.0, 0.5)
    sb6 = SpaceBike(197567, 'Nova Bike', 0, 8.0, 0.5)
    sb7 = SpaceBike(198732, 'Nova Bike', 1, 8.0, 0.5)
    sb_list = [sb1, sb2, sb3, sb4, sb5, sb6, sb7]
    sorted_list = _sb_priority_capacity(sb_list)
    assert sorted_list[0] == sb2
    assert sorted_list[1] == sb7

def test_nr_bogo_for_board():
    dmap = DistanceMap()
    dmap.add_distance("Earth", "Mars", 1.0)
    dmap.add_distance("Mars", "Tihuania", 20.0)

    sf = SpaceFleet()

    p1 = Passenger("Halo,", 1.0, "Earth", "Earth")
    sb1 = SpaceBike(198761, 'Nova Bike', 2, 8.0, 0.5) # passenger source in travel_chart

    p2 = Passenger("Bello", 1.0, "Earth", "Mars")
    sb1.travel_chart = [('Earth', 'Mars')] # passenger route in travel chart

    p3 = Passenger("Cello", 1.0, "Earth", "Tihuania")  # will not pass, insufficient fuel

    p4 = Passenger("Dello", 1.0, "Celvo", "Mars")  # will not pass, source not in route

    p5 = Passenger("Illo", 1.0, "Earth", "Mars")  # will not pass, bike capacity is 0

    passengers = [p1, p2, p3, p4, p5]
    sf.add_space_bike(sb1)

    b_scheduler = BogoScheduler(sf, dmap)
    b_scheduler.schedule(passengers, sf.bikes)
    assert sb1.travel_chart == [('Earth', 'Mars')]
    assert sb1.curr_capacity == 0
    assert p3 not in sb1.passenger_list
    assert p4 not in sb1.passenger_list

def test_greedy_load_queue():
    dmap = DistanceMap()
    dmap.add_distance("Earth", "Mars", 1.0)
    dmap.add_distance("Mars", "Tihuania", 20.0)

    p1 = Passenger("Halo,", 0.0, "Earth", "Earth")
    p2 = Passenger("Halo,,", 10.0, "Earth", "Earth")
    p3 = Passenger("Halo,,,", 0.0, "Earth", "Earth")
    p4 = Passenger("Halo,,,,", 10.0, "Earth", "Earth")
    p5 = Passenger("Halo,,,,,", 2.0, "Earth", "Earth")
    p6 = Passenger("Halo,,,,,,", 3.57, "Earth", "Earth")
    p7 = Passenger("Halo,,,,,,,", 2.0, "Earth", "Earth")

    p_list = [p1, p2, p3, p4, p5, p6, p7]
    scheduler = GreedyScheduler(dmap, 'fare_bid')
    p_queue = scheduler._load_queue(p_list)
    assert p_queue._first.val == p2
    assert p_queue._first.next.val == p4
    assert p_queue._first.next.next.val == p6
    assert p_queue._first.next.next.next.val == p5
    assert p_queue._first.next.next.next.next.val == p7
    assert p_queue._first.next.next.next.next.next.val == p1
    assert p_queue._first.next.next.next.next.next.next.val == p3

def test_sb_id_sort():
    dmap = DistanceMap()
    dmap.add_distance("Earth", "Mars", 1.0)
    dmap.add_distance("Earth", "Mercury", 1.0)
    dmap.add_distance("Earth", "Fr18", 1.0)
    dmap.add_distance("Earth", "Juniper", 1.0)
    dmap.add_distance("Earth", "J4l4pinyos", 230.0)
    dmap.add_distance("Earth", "Neptune", 1.0)
    dmap.add_distance("Mercury", "Mars", 1.0)
    dmap.add_distance("Mars", "Jupiter", 1.0)
    dmap.add_distance("Mars", "J4l4pinyos", 230.0)
    dmap.add_distance("Jupiter", "Neptune", 1.5)
    dmap.add_distance("Jupiter", "Fr18", 1.0)
    dmap.add_distance("Fr18", "Neptune", 1.0)
    dmap.add_distance("Fr18", "Mars", 1.0)
    dmap.add_distance("Mars", "Neptune", 1.0)
    dmap.add_distance("Molestus", "Mars", 1.0)
    dmap.add_distance("Mercury", "Jupiter", 1.0)
    dmap.add_distance("Neptune", "Juniper", 1.0)
    dmap.add_distance("Mars", "Juniper", 1.0)
    dmap.add_distance("Mars", "Molestus", 3.0)
    dmap.add_distance("Neptune", "Molestus", 2.0)
    dmap.add_distance("Neptune", "J4l4pinyos", 230.0)
    dmap.add_distance("Jupiter", "Molestus", 1.0)
    dmap.add_distance("Juniper", "J4l4pinyos", 1.0)
    dmap.add_distance("Jupiter", "J4l4pinyos", 1.0)
    dmap.add_distance("Molestus", "J4l4pinyos", 230.0)
    dmap.add_distance("Crowayshi,a", "Mercury", 1.0)

    p1 = Passenger("Halo,", 0.0, "Earth", "Juniper")

    sb0 = SpaceBike(10222000, "Nova Bike", 1, 8.0, 0.5)
    sb0.travel_chart = [("Earth", "Mars")]

    sb1 = SpaceBike(102001, "Nova Bike", 1, 8.0, 0.5)
    sb1.travel_chart = [("Earth", "Mars")]

    sb2 = SpaceBike(101002, "Nova Bike", 1, 8.0, 0.5)
    sb2.travel_chart = [("Earth", "Mars")]

    sb3 = SpaceBike(1012003, "Nova Bike", 1, 8.0, 0.5)
    sb3.travel_chart = [("Earth", "Mars")]

    sb4 = SpaceBike(100104, "Nova Bike", 1, 8.0, 0.5)
    sb4.travel_chart = [("Earth", "Mars")]

    sb5 = SpaceBike(5, "Nova Bike", 1, 8.0, 0.5)
    sb5.travel_chart = [("Earth", "Mars")]

    space_bikes = [sb0, sb1, sb2, sb3, sb4, sb5]

    assert _space_bike_priority(p1, space_bikes, dmap).id == sb5.id

def test_priority_queue_fuel():
    dmap = DistanceMap()
    dmap.add_distance("Earth", "Mars", 1.0)
    dmap.add_distance("Earth", "Mercury", 1.0)
    dmap.add_distance("Earth", "Fr18", 1.0)
    dmap.add_distance("Earth", "Juniper", 2.0)
    dmap.add_distance("Earth", "J4l4pinyos", 0.1)
    dmap.add_distance("Earth", "Neptune", 1.0)
    dmap.add_distance("Mercury", "Mars", 1.0)
    dmap.add_distance("Mars", "Jupiter", 1.0)
    dmap.add_distance("Mars", "J4l4pinyos", 230.0)
    dmap.add_distance("Jupiter", "Neptune", 1.5)
    dmap.add_distance("Jupiter", "Fr18", 1.0)
    dmap.add_distance("Fr18", "Neptune", 1.0)
    dmap.add_distance("Fr18", "Mars", 1.0)
    dmap.add_distance("Mars", "Neptune", 1.0)
    dmap.add_distance("Molestus", "Mars", 1.0)
    dmap.add_distance("Mercury", "Jupiter", 1.0)
    dmap.add_distance("Neptune", "Juniper", 2.0)
    dmap.add_distance("Mars", "Juniper", 5.0)
    dmap.add_distance("Mars", "Molestus", 3.0)
    dmap.add_distance("Neptune", "Molestus", 2.0)
    dmap.add_distance("Neptune", "J4l4pinyos", 230.0)
    dmap.add_distance("Jupiter", "Molestus", 1.0)
    dmap.add_distance("Juniper", "J4l4pinyos", 3.0)
    dmap.add_distance("Jupiter", "J4l4pinyos", 1.0)
    dmap.add_distance("Molestus", "J4l4pinyos", 230.0)
    dmap.add_distance("Crowayshi,a", "Mercury", 1.0)

    p1 = Passenger("Halo,", 0.0, "Earth", "Juniper")

    sb0 = SpaceBike(10222000, "Nova Bike", 1, 8.0, 3)
    sb0.travel_chart = [("Earth",)]

    sb1 = SpaceBike(102001, "Nova Bike", 1, 0.5, 0.5)
    sb1.travel_chart = [("Earth", "Neptune")]

    sb2 = SpaceBike(101002, "Nova Bike", 1, 8.0, 0.5)
    sb2.travel_chart = [("Earth", "J4l4pinyos")]

    sb3 = SpaceBike(1012003, "Nova Bike", 1, 8.0, 0.5)
    sb3.travel_chart = [("Earth", "Mars")]

    # sb4 = SpaceBike(100104, "Nova Bike", 1, 8.0, 0.5)
    # sb4.travel_chart = [("Earth", "Mars")]
    #
    # sb5 = SpaceBike(5, "Nova Bike", 1, 8.0, 0.5)
    # sb5.travel_chart = [("Earth", "Mars")]

    space_bikes = [sb0, sb1, sb2, sb3]
    assert _sb_priority_fuel(p1, dmap, space_bikes).id == sb2.id

def test_enroute():
    p1 = Passenger("Halo,", 0.0, "J4l4pinyos", "J4l4pinyos")

    sb0 = SpaceBike(10222000, "Nova Bike", 1, 8.0, 3)
    sb0.travel_chart = [("Earth",)]

    sb1 = SpaceBike(102001, "Nova Bike", 1, 0.5, 0.5)
    sb1.travel_chart = [("Earth", "Neptune")]

    sb2 = SpaceBike(101002, "Nova Bike", 1, 8.0, 0.5)
    sb2.travel_chart = [("Earth", "J4l4pinyos"), ("J4l4pinyos", "Neptune")]

    sb3 = SpaceBike(1012003, "Nova Bike", 1, 8.0, 0.5)
    sb3.travel_chart = [("Earth", "Mars"), ("Mars", "J4l4pinyos")]

    space_bikes = [sb0, sb1, sb2, sb3]

    assert _return_bike_enroute_poss_bikes(p1,space_bikes) == sb2

if __name__ == "__main__":
    import pytest
    pytest.main(['starter_tests_a2.py'])
