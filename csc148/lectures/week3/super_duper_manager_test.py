"""CSC148 in-class exercise: Super Duper Manager

=== Module description ===
This module contains sample tests for an in-class exercise.

Warning: This is an extremely incomplete set of tests!
Add your own to practice writing tests and to be confident your code is correct.
"""
from hypothesis import given, assume
from hypothesis.strategies import integers, text
from sdm import SuperDuperManager


@given(text(min_size=1), integers(min_value=1, max_value=100000))
def test_new_car_attributes(id_, fuel):
    manager = SuperDuperManager()
    manager.add_vehicle('Car', id_, fuel)
    assert manager.get_vehicle_fuel(id_) == fuel
    assert manager.get_vehicle_position(id_) == (0, 0)


@given(text(min_size=1), integers(min_value=1, max_value=100000))
def test_new_helicopter_attributes(id_, fuel):
    manager = SuperDuperManager()
    manager.add_vehicle('Helicopter', id_, fuel)
    assert manager.get_vehicle_fuel(id_) == fuel
    assert manager.get_vehicle_position(id_) == (3, 5)


@given(text(min_size=1), integers(min_value=1, max_value=100000))
def test_new_carpet_attributes(id_, fuel):
    manager = SuperDuperManager()
    manager.add_vehicle('UnreliableMagicCarpet', id_, fuel)
    assert manager.get_vehicle_fuel(id_) == fuel
    pos = manager.get_vehicle_position(id_)
    assert abs(pos[0]) <= 10
    assert abs(pos[1]) <= 10


@given(text(min_size=1), integers(min_value=1),
       integers(min_value=-200, max_value=200),
       integers(min_value=-200, max_value=200))
def test_move_car_changes_attributes(id_, fuel, new_x, new_y):
    # Similar to an assert: retries test when this property is false
    assume(abs(new_x) + abs(new_y) <= fuel)

    manager = SuperDuperManager()
    manager.add_vehicle('Car', id_, fuel)
    manager.move_vehicle(id_, new_x, new_y)
    assert manager.get_vehicle_position(id_) == (new_x, new_y)
    assert manager.get_vehicle_fuel(id_) == fuel - abs(new_x) - abs(new_y)


if __name__ == '__main__':
    import pytest
    pytest.main()
