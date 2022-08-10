"""
=== Assignment 1 ===
CSC148, Summer 2021

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Marina Tawfik, Saima Ali.

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 Marina Tawfik, Saima Ali.
"""
import pytest
from pokemon import Pokemon, Trainer, PokeCenter, World, \
    load_trainers, load_pokemon_weakness, load_pokemon_types


################################################################################
# Sample test cases below
#
# Use the test cases below as an example for writing your own test cases,
# and as a start to testing your A1 code. Most of these test functions create
# objects "by hand" that are used for testing methods.  Once you implement
# function load_trainers, you will be able to populate the world with many
# trainers by calling load_trainers. You may find this makes testing easier.
#
# The self-test on MarkUs runs the tests below, along with a few others.
# Make sure you run the self-test on MarkUs after submitting your code!
#
# You do not have to submit this file for A1. This is for your own use.
#
# WARNING: THIS IS CURRENTLY AN EXTREMELY INCOMPLETE SET OF TESTS!
# We will test your code on a much more thorough set of tests!
################################################################################


def test_get_all_pokemon():
    """Test that get_all_pokemon return a shallow copy of the _pokemon list
    """
    pikachu = Pokemon("Pikachu", "electric", {"ground": 1.0}, 1, 100, 10, 5)
    bulbasaur = Pokemon(
        "Bulbasaur", "grass",
        {"fire" : 1.0, "psychic": 0.5, "flying": 0.3, "ice": 0.1},
        1, 100, 10, 5
    )
    squirtle = Pokemon(
        "Squirtle", "water", {"grass" : 0.5, "electric": 0.7}, 1, 100,
        10, 5
    )

    trainer1 = Trainer("Ash")

    trainer1.add_pokemon(pikachu)
    trainer1.add_pokemon(bulbasaur)
    trainer1.add_pokemon(squirtle)

    trainer_pokemon = trainer1.get_all_pokemon()

    trainer_pokemon.remove(pikachu)
    trainer_pokemon = trainer1.get_all_pokemon()

    assert len(trainer_pokemon) == 3 and pikachu in trainer_pokemon and \
        bulbasaur in trainer_pokemon and squirtle in trainer_pokemon, \
        "calling get_all_pokemon() should return a copy of the pokemon owned " \
        "by trainer."


def test_choose_pokemon():
    """Test choose_pokemon when the highest-level Pokemon is not available.
    """
    pikachu = Pokemon("Pikachu", "electric", {"ground": 1.0}, 70, 100, 10, 5)
    pikachu.curr_hp = 0
    pikachu.fainted = True

    bulbasaur = Pokemon(
        "Bulbasaur", "grass",
        {"fire": 1.0, "psychic": 0.5, "flying": 0.3, "ice": 0.1},
        10, 100, 10, 5
    )
    squirtle = Pokemon(
        "Squirtle", "water", {"grass": 0.5, "electric": 0.7},
        30, 100, 10, 5
    )

    sandshrew = Pokemon(
        "Sandshrew", "ground", {"water": 0.1, "grass": 0.5, "ice": 0.1},
        20, 100, 5, 15
    )

    trainer1 = Trainer("Ash")
    trainer1.add_pokemon(pikachu)
    trainer1.add_pokemon(bulbasaur)
    trainer1.add_pokemon(squirtle)

    selected_pokemon = trainer1.choose_pokemon(sandshrew)

    assert selected_pokemon == squirtle, \
        "Trainer should select the highest-level available pokemon that " \
        "provides the highest advantage"

def test_choose_pokemon_no_poke():
    """Test choose_pokemon when the trainer has no pokemon.
    """
    pikachu = Pokemon("Pikachu", "electric", {"ground": 1.0}, 70, 100, 10, 5)
    pikachu.curr_hp = 0
    pikachu.fainted = True

    bulbasaur = Pokemon(
        "Bulbasaur", "grass",
        {"fire": 1.0, "psychic": 0.5, "flying": 0.3, "ice": 0.1},
        10, 100, 10, 5
    )
    squirtle = Pokemon(
        "Squirtle", "water", {"grass": 0.5, "electric": 0.7},
        30, 100, 10, 5
    )

    sandshrew = Pokemon(
        "Sandshrew", "ground", {"water": 0.1, "grass": 0.5, "ice": 0.1},
        20, 100, 5, 15
    )

    trainer1 = Trainer("Ash")

    selected_pokemon = trainer1.choose_pokemon(sandshrew)

    assert selected_pokemon == None, \
        "Trainer should select the highest-level available pokemon that " \
        "provides the highest advantage"


def test_record_battle_outcome_and_get_win_rate():
    """Test get_win_rate when a trainer has not participated in any battles.
    """
    trainer1 = Trainer("Ash")
    trainer2 = Trainer("Misty")
    trainer3 = Trainer("Brock")

    trainer1.record_battle_outcome(trainer2, True)
    trainer1.record_battle_outcome(trainer2, True)
    trainer1.record_battle_outcome(trainer2, True)
    trainer1.record_battle_outcome(trainer2, False)

    trainer2.record_battle_outcome(trainer1, False)
    trainer2.record_battle_outcome(trainer1, False)
    trainer2.record_battle_outcome(trainer1, False)
    trainer2.record_battle_outcome(trainer1, True)

    actual_result = (
        trainer1.get_win_rate(),
        trainer2.get_win_rate(),
        trainer3.get_win_rate()
    )
    expected_result = (0.8, 0.2, None)

    assert actual_result == expected_result,\
        "get_win_rate should return the number of battles won over the total " \
        "number of battles, rounded to the tenth decimal place and " \
        "return None if the trainer has not participated in any battles."


def test_pokecenter_admit_discharge_and_get_availability():
    """Test that we can admit and discharge several pokemon from a pokecenter.
    """
    pokecenter = PokeCenter("PC1", 5)

    pikachu = Pokemon("Pikachu", "electric", {"ground": 1.0}, 1, 100, 10, 5)
    bulbasaur = Pokemon(
        "Bulbasaur", "grass",
        {"fire": 1.0, "psychic": 0.5, "flying": 0.3, "ice": 0.1},
        1, 100, 10, 5
    )
    squirtle = Pokemon(
        "Squirtle", "water", {"grass": 0.5, "electric": 0.7},
        1, 100, 10, 5
    )
    pidgeotto = Pokemon(
        "Pidgeotto", "flying", {"electric": 0.5, "ice": 1.0, "rock": 0.5},
        1, 100, 10, 5
    )

    pokecenter.admit_pokemon(pikachu)
    pokecenter.admit_pokemon(bulbasaur)
    pokecenter.admit_pokemon(squirtle)
    pokecenter.discharge_pokemon(bulbasaur)
    pokecenter.discharge_pokemon(squirtle)
    pokecenter.admit_pokemon(pidgeotto)

    assert pokecenter.get_availability() == 3 and pikachu.in_hospital \
        and not bulbasaur.in_hospital and not squirtle.in_hospital \
        and pidgeotto.in_hospital, \
        "Admit and discharge pokemon should update the Pokecenter's " \
        "collection of admitted Pokemon as well as change the Pokemon status."


def test_rank_trainers():
    main_player = Trainer("CSC148-class")
    world = World(main_player)

    trainer1 = Trainer("Ash")
    trainer2 = Trainer("Misty")
    trainer3 = Trainer("Brock")

    world.add_trainer(trainer1)
    world.add_trainer(trainer2)
    world.add_trainer(trainer3)

    trainer1.record_battle_outcome(trainer2, True)
    trainer2.record_battle_outcome(trainer1, False)

    trainer1.record_battle_outcome(trainer2, False)
    trainer2.record_battle_outcome(trainer1, True)

    trainer1.record_battle_outcome(trainer3, True)
    trainer3.record_battle_outcome(trainer1, False)

    trainer1.record_battle_outcome(trainer3, True)
    trainer3.record_battle_outcome(trainer1, False)

    trainer1.record_battle_outcome(trainer3, True)
    trainer3.record_battle_outcome(trainer1, False)

    trainer2.record_battle_outcome(trainer3, False)
    trainer3.record_battle_outcome(trainer2, True)

    trainer1.record_battle_outcome(trainer2, True)
    trainer2.record_battle_outcome(trainer1, False)

    result = world.rank_trainers()
    assert len(result) == 2 \
        and len(result[0]) == 1 and trainer1 in result[0] \
        and len(result[1]) == 2 and trainer2 in result[1] \
        and trainer3 in result[1],\
        "calling rank_trainers() should return a tier list of trainer ranks"


def test_admit_all_npc_pokemon():
    """Test admit_all_npc_pokemon when there is exactly one other non-player
    trainer with more Pokemon than that accepted limit.
    """
    player = Trainer("CSC148-trainer")
    world = World(player)

    ash = Trainer("Ash")
    world.add_trainer(ash)

    # Player's Pokemon
    torchic = Pokemon(
        "Torchic", "fire", {"water": 0.5, "ground": 0.1, "rock": 0.1},
        5, 100, 10, 5
    )
    torchic.curr_hp = 0
    torchic.fainted = True
    world.add_pokemon(torchic)
    player.add_pokemon(torchic)

    # Ash's Pokemon
    bulbasaur = Pokemon(
        "Bulbasaur", "grass",
        {"fire": 1.0, "psychic": 0.5, "flying": 0.3, "ice": 0.1},
        10, 100, 10, 5
    )
    bulbasaur.curr_hp = 60

    squirtle = Pokemon(
        "Squirtle", "water", {"grass": 0.5, "electric": 0.7},
        30, 100, 10, 5
    )
    squirtle.curr_hp = 50

    for pokemon in [bulbasaur, squirtle]:
        world.add_pokemon(pokemon)
        ash.add_pokemon(pokemon)

    pokecenter1 = PokeCenter("PC1", 20)
    world.add_pokecenter(pokecenter1)

    world.admit_all_npc_pokemon(1)

    assert pokecenter1.get_availability() == 19 \
        and pokecenter1.is_admitted(squirtle) \
        and not pokecenter1.is_admitted(bulbasaur),\
        "admit_all_npc_pokemon() should only send the Pokemon of non-player" \
        "trainers and should follow the specified limit."


def test_load_trainers():
    """Test load_trainers on pokemon_trainers.txt
    """
    player = Trainer("CSC148-Player")
    world = World(player)

    with open('pokemon_data/pokemon_names.txt') as f_pokemon_types:
        world._type_to_name_mapping = load_pokemon_types(f_pokemon_types)

    with open('pokemon_data/pokemon_weaknesses.txt') as f_pokemon_weakness:
        world._type_to_weakness_mapping = \
            load_pokemon_weakness(f_pokemon_weakness)

    with open('pokemon_data/pokemon_trainers.txt') as f_trainers:
        load_trainers(f_trainers, world)

    assert len(world._trainers) == 4, \
        "Trainers list haven't been populated properly"

    assert len(world._trainers[1].get_all_pokemon()) == 4
    assert world._pokemon[-1].name == 'Weezing'
    assert world._pokemon[-1].defense_points == 15
    assert world._pokemon[-1].weakness['poison'] == 0.5
    assert world._pokemon[-1].type == 'fairy'
    # Note: You may want to check more properties below!
    #       The current test just checks that number of trainers is 3
    #       as expected


def test_choose_pokemon_no_advtge_type():
    """Tests that Trainer.choose_pokemon returns the pokemon with the highest level
    when no pokemon has an advantage over the opp_pokemon"""

    pikachu = Pokemon( "Pikachu", "electric", {"ground": 1.0}, 7, 100, 10, 5 )
    squirtle = Pokemon( "Squirtle", "poison", {"grass" : 0.5, "electric": 0.7},\
               5, 100, 10, 5)
    bulbasaur = Pokemon( "Bulbasaur", "fire",\
                         {"fire" : 1.0, "psychic": 0.5, "flying": 0.3, "ice": 0.1},\
                         1, 100, 10, 5 )
    sandshrew = Pokemon("Sandshrew", "ground", {"water": 0.1, "grass": 0.5, "ice": 0.1},\
                        1, 100, 5, 15)

    ash = Trainer("Ash", 1, 5, 15)
    ash.add_pokemon(pikachu)
    ash.add_pokemon(squirtle)
    ash.add_pokemon(bulbasaur)

    assert ash.choose_pokemon(sandshrew).name == "Pikachu"


def test_choose_pokemon_no_opp():
    """Tests that Trainer.choose_pokemon returns the pokemon with the last best
    type advantage when none of the other pokemon have an advantage
    """
    pikachu = Pokemon( "Pikachu", "electric", {"ground": 1.0}, 7, 100, 10, 5 )
    squirtle = Pokemon( "Squirtle", "poison", {"grass" : 0.5, "electric": 0.7}, \
                        5, 100, 10, 5)
    bulbasaur = Pokemon( "Bulbasaur", "ice", \
                         {"fire" : 1.0, "poison": 0.5, "flying": 0.3, "ice": 0.1}, \
                         1, 100, 10, 5 )
    sandshrew = Pokemon("Sandshrew", "ground", {"water": 0.1, "grass": 0.5, "ice": 0.1}, \
                        1, 100, 5, 15)

    ash = Trainer("Ash", 1, 5, 15)
    ash.add_pokemon(pikachu)
    ash.add_pokemon(squirtle)
    ash.add_pokemon(bulbasaur)

    assert ash.choose_pokemon(None).name == "Pikachu"
#
def test_choose_same_level_no_type_weakness():
    """Tests that Trainer.choose_pokemon returns the pokemon with the last best
    type advantage when none of the other pokemon have an advantage
    """
    pikachu = Pokemon( "Pikachu", "electric", {"ground": 1.0}, 7, 100, 10, 5 )
    bulbasaur = Pokemon( "Bulbasaur", "fire", \
                         {"fire" : 1.0, "poison": 0.5, "flying": 0.3, "ice": 0.1}, \
                         7, 100, 10, 5 )
    squirtle = Pokemon( "Squirtle", "poison", {"grass" : 0.5, "electric": 0.7}, \
                        7, 100, 10, 5)
    sandshrew = Pokemon("Sandshrew", "ground", {"water": 0.1, "grass": 0.5, "ice": 0.1}, \
                        7, 100, 5, 15)

    ash = Trainer("Ash", 1, 5, 15)
    ash.add_pokemon(pikachu)
    ash.add_pokemon(bulbasaur)
    ash.add_pokemon(squirtle)

    assert ash.choose_pokemon(sandshrew).name in ['Pikachu', 'Bulbasaur', 'Squirtle']

def test_choose_same_level_with_type_weakness():
    """Tests that Trainer.choose_pokemon returns the pokemon with the last best
    type advantage when none of the other pokemon have an advantage
    """
    pikachu = Pokemon( "Pikachu", "electric", {"ground": 1.0}, 7, 100, 10, 5 )
    bulbasaur = Pokemon( "Bulbasaur", "water", \
                         {"fire" : 1.0, "poison": 0.5, "flying": 0.3, "ice": 0.1}, \
                         7, 100, 10, 5 )
    squirtle = Pokemon( "Squirtle", "water", {"grass" : 0.5, "electric": 0.7}, \
                        7, 100, 10, 5)
    sandshrew = Pokemon("Sandshrew", "ground", {"water": 0.1, "grass": 0.5, "ice": 0.1}, \
                        7, 100, 5, 15)

    ash = Trainer("Ash", 1, 5, 15)
    ash.add_pokemon(pikachu)
    ash.add_pokemon(bulbasaur)
    ash.add_pokemon(squirtle)

    assert ash.choose_pokemon(sandshrew).name in ['Bulbasaur', 'Squirtle']
#
def test_choose_with_one_fainted_one_hospital():
    """Tests that Trainer.choose_pokemon returns the pokemon with the last best
    type advantage when none of the other pokemon have an advantage
    """
    pikachu = Pokemon( "Pikachu", "fire", {"ground": 1.0}, 7, 100, 10, 5 )
    bulbasaur = Pokemon( "Bulbasaur", "water", \
                         {"fire" : 1.0, "poison": 0.5, "flying": 0.3, "ice": 0.1}, \
                         70, 100, 10, 5 )
    squirtle = Pokemon( "Squirtle", "water", {"grass" : 0.5, "electric": 0.7}, \
                        7, 100, 10, 5)
    sandshrew = Pokemon("Sandshrew", "ground", {"water": 0.1, "grass": 0.5, "ice": 0.1}, \
                        7, 100, 5, 15)
    bulbasaur.fainted = True
    squirtle.in_hospital = True
    ash = Trainer("Ash", 1, 5, 15)
    ash.add_pokemon(pikachu)
    ash.add_pokemon(bulbasaur)
    ash.add_pokemon(squirtle)

    assert ash.choose_pokemon(sandshrew).name == 'Pikachu'

def test_record_battle_win_rate():
    """Check if record_battle and get_win_rate work properly"""

    ash = Trainer("Ash", 1, 5, 15)
    misty = Trainer("Misty", 1, 5, 15)
    clancy = Trainer("Clancy", 1, 5, 15)

    assert ash.get_win_rate() is None
    assert misty.get_win_rate() is None

    ash.record_battle_outcome(misty, False)
    misty.record_battle_outcome(ash, True)

    assert ash.get_win_rate() == 0.0
    assert misty.get_win_rate() == 1.0

    ash.record_battle_outcome(misty, True)
    misty.record_battle_outcome(ash, False)

    assert ash.get_win_rate() == 0.5
    misty.get_win_rate() == 0.5

    clancy.record_battle_outcome(misty, False)
    misty.record_battle_outcome(clancy, True)
    clancy.record_battle_outcome(ash, True)
    ash.record_battle_outcome(clancy, False)

    assert clancy.get_win_rate() == 0.5
    assert ash.get_win_rate() == 0.3
    assert misty.get_win_rate() == 0.7

def test_admit_pokemon_get_availability_discharge():
    pokecenter = PokeCenter("PC1", 2)
    pikachu = Pokemon("Pikachu", "electric", {"ground": 1.0}, 1, 100, 10, 5)
    pikachu.curr_hp = int(0.5 * pikachu.max_hp)
    vinyl = Pokemon("Vinyl", "poison", {"ground": 1.0}, 1, 100, 10, 5)
    vinyl.curr_hp = int(0.5 * vinyl.max_hp)
    charizard = Pokemon("Charizard", "poison", {"ground": 1.0}, 1, 100, 10, 5)
    assert pokecenter.admit_pokemon(pikachu) == True
    assert pikachu.in_hospital == True
    assert pokecenter.get_availability() == 1
    assert pokecenter.is_admitted(pikachu)
    assert pokecenter.admit_pokemon(vinyl)
    assert pokecenter.get_availability() == 0
    assert not pokecenter.admit_pokemon(charizard)
    assert not pokecenter.discharge_pokemon(charizard)
    pokecenter.heal_admitted_pokemon()
    assert pokecenter.discharge_pokemon(pikachu)
    assert pikachu.in_hospital == False
    assert vinyl.curr_hp == vinyl.max_hp
    assert pikachu.curr_hp == pikachu.max_hp
    assert pikachu not in pokecenter._admitted_pokemon
    assert pokecenter.get_availability() == 1
    assert pokecenter.admit_pokemon(charizard)

def test_init_rank_trainers():
    player = Trainer("CSC148-trainer", 1, 5, 15)
    world = World(player)
    assert world._trainers == [player]

    ash = Trainer("Ash", 1, 5, 15)
    misty = Trainer("Misty", 1, 5, 15)
    brock = Trainer("Brock", 1, 5, 15)
    world.add_trainer(ash)
    world.add_trainer(misty)
    world.add_trainer(brock)
    assert world._trainers == [player, ash, misty, brock]

    pikachu = Pokemon("Pikachu", "electric", {"ground": 1.0}, 1, 100, 10, 5)
    ash.add_pokemon(pikachu)
    butterfree = Pokemon("Butterfree", "bug", {"fire": 1.0, "flying": 0.5, "rock": 0.2},\
                         1, 100, 10, 5)
    world.add_pokemon(pikachu)
    world.add_pokemon(butterfree)

    misty.add_pokemon(butterfree)

    ash.record_battle_outcome(misty, True)
    misty.record_battle_outcome(ash, False)
    misty.record_battle_outcome(ash, True)
    ash.record_battle_outcome(misty, False)
    result = world.rank_trainers()
    assert result == [[ash, misty]]

    assert ash in result[0]
    assert misty in result[0]
    assert brock not in result[0]

    player.add_pokemon(pikachu)
    player.record_battle_outcome(ash, True)
    ash.record_battle_outcome(player, False)

    brock.add_pokemon(butterfree)
    brock.record_battle_outcome(misty, False)
    misty.record_battle_outcome(brock, True)

    assert player.get_win_rate() == 1
    assert misty.get_win_rate() == 0.7
    assert ash.get_win_rate() == 0.3
    assert brock.get_win_rate() == 0

    assert world.rank_trainers() == [[player], [misty], [ash], [brock]]
    lst = []
    ranking = world.rank_trainers()
    for trainer_list in ranking:
        for trainer in trainer_list:
            lst.append(trainer.name)
    assert lst == ['Csc148-Trainer', 'Misty', 'Ash', 'Brock']

    josh = Trainer("Josh", 1, 5, 15)
    josh.add_pokemon(pikachu)
    world.add_trainer(josh)
    josh.record_battle_outcome(brock, True)
    assert world.rank_trainers() == [[player, josh], [misty], [ash], [brock]]

    assert len(world._trainers) == 5
    assert len(world._pokemon) == 2
    assert len(josh.get_all_pokemon()) == 1
    assert len(ash.get_all_pokemon()) == 1
    assert len(brock.get_all_pokemon()) == 1
    assert len(misty.get_all_pokemon()) == 1

def test_admit_all_pokemon():
    """Test admit_admit_all_pokemon"""

    player = Trainer("CSC148-trainer")
    world = World(player)

    pokecenter1 = PokeCenter("PC1", 2)
    pokecenter2 = PokeCenter("PC2", 1)

    world.add_pokecenter(pokecenter1)
    world.add_pokecenter(pokecenter2)

    ash = Trainer("Ash")
    jeff = Trainer("Jeff")

    pikachu = Pokemon( \
        "Pikachu", "electric", {"ground": 1.0}, 1, 100, 10, 5)
    squirtle = Pokemon( \
        "Squirtle", "water", {"grass" : 0.5, "electric": 0.7}, 1, 100, \
        10, 5)
    charzar = Pokemon( \
        "Charzar", "water", {"grass" : 0.5, "electric": 0.7}, 1, 100, \
        10, 5)
    dialga = Pokemon( \
        "Dialga", "dragon", {"grass" : 0.5, "electric": 0.7}, 1, 100, \
        10, 5)
    vinyl = Pokemon( \
        "Vinyl", "Poison", {"grass" : 0.5, "electric": 0.7}, 1, 100, \
        10, 5)
    bulbasaur = Pokemon( \
        "Bulbasaur", "grass", \
        {"fire" : 1.0, "psychic": 0.5, "flying": 0.3, "ice": 0.1}, \
        1, 100, 10, 5 \
    )

    world.add_trainer(ash)
    world.add_trainer(jeff)

    world.add_pokemon(squirtle)
    world.add_pokemon(pikachu)
    world.add_pokemon(bulbasaur)
    world.add_pokemon(dialga)
    world.add_pokemon(charzar)
    world.add_pokemon(vinyl)

    ash.add_pokemon(squirtle)
    ash.add_pokemon(pikachu)
    ash.add_pokemon(bulbasaur)

    jeff.add_pokemon(charzar)
    jeff.add_pokemon(dialga)
    jeff.add_pokemon(vinyl)

    # player.add_pokemon(bulbasaur)

    squirtle.curr_hp = 80 #pokecenter1
    squirtle.fainted = False
    pikachu.curr_hp = 60 #pokecenter2
    pikachu.fainted = False
    bulbasaur.curr_hp = 95 #no pokecenter because of limit
    bulbasaur.fainted = False
    charzar.curr_hp = 100 #no pokecenter full health
    charzar.fainted = False
    dialga.curr_hp = 95 #pokecenter1
    dialga.fainted = False
    vinyl.curr_hp = 95 #no pokecenter alphabetical order
    vinyl.fainted = False

    world.admit_all_npc_pokemon(2)
    assert pikachu.in_hospital

    assert pokecenter1.is_admitted(squirtle)
    assert pokecenter2.is_admitted(pikachu)
    assert pokecenter1.is_admitted(dialga)
    assert not bulbasaur.in_hospital
    assert not charzar.in_hospital
    assert not vinyl.in_hospital

    # assert not bulbasaur.in_hospital  # owned by player

    assert pokecenter1.get_availability() == 0
    assert pokecenter2.get_availability() == 0

def test_admit_all_pokemon_no_mutation():
    """Test admit_admit_all_pokemon"""

    player = Trainer("CSC148-trainer")
    world = World(player)

    pokecenter1 = PokeCenter("PC1", 2)
    pokecenter2 = PokeCenter("PC2", 1)

    world.add_pokecenter(pokecenter1)
    world.add_pokecenter(pokecenter2)

    ash = Trainer("Ash")

    pikachu = Pokemon( \
        "Pikachu", "electric", {"ground": 1.0}, 1, 100, 10, 5)
    squirtle = Pokemon( \
        "Squirtle", "water", {"grass" : 0.5, "electric": 0.7}, 1, 100, \
        10, 5)
    bulbasaur = Pokemon( \
        "Bulbasaur", "grass", \
        {"fire" : 1.0, "psychic": 0.5, "flying": 0.3, "ice": 0.1}, \
        1, 100, 10, 5 \
        )

    world.add_trainer(ash)

    world.add_pokemon(squirtle)
    world.add_pokemon(pikachu)
    world.add_pokemon(bulbasaur)

    ash.add_pokemon(squirtle)
    ash.add_pokemon(pikachu)

    player.add_pokemon(bulbasaur)

    pikachu.curr_hp = 0
    pikachu.fainted = True
    squirtle.curr_hp = 0
    squirtle.fainted = True
    bulbasaur.curr_hp = 0
    bulbasaur.fainted = True

    world.admit_all_npc_pokemon(3)
    assert pikachu.in_hospital

    assert not pokecenter1.is_admitted(pikachu)
    assert pokecenter2.is_admitted(pikachu)
    assert squirtle.in_hospital  # tied for hp, admit in alphabetical order
    assert not bulbasaur.in_hospital  # owned by player

    assert pokecenter1.get_availability() == 1
    assert pokecenter2.get_availability() == 0

    assert world._trainers == [player, ash]
    assert world._pokemon == [squirtle, pikachu, bulbasaur]
    assert world._pokecenters == [pokecenter1, pokecenter2]
    assert ash.get_all_pokemon() == [squirtle, pikachu]
    assert player.get_all_pokemon() == [bulbasaur]

if __name__ == '__main__':
    pytest.main(['a1_starter_tests.py'])
