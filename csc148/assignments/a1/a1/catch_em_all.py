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

from __future__ import annotations
import os
import random
from typing import List, Any, Optional, Callable, TextIO, Dict, Tuple
import datetime
import time

import pokemon as poke


INIT_NUM_WILD_POKEMON = 100
UPDATE_NUM_WILD_POKEMON = 50
NUM_POKECENTERS = 4
MIN_POKECENTER_CAPACITY, MAX_POKECENTER_CAPACITY = 3, 10
WILD_MIN_HP, WILD_MAX_HP = 30, 90
WILD_MIN_ATK, WILD_MAX_ATK = 5, 40
WILD_MIN_DEF, WILD_MAX_DEF = 5, 40
MAX_BATTLE_POKEMON = 3
POKEBALL_COST = 10
POKECENTER_TRAINER_LIMIT = 3


class Pokemon(poke.Pokemon):
    """A more complete representation of a Pokemon."""
    name: str
    type: str
    weakness: Dict[str, float]
    attack_points: int
    defense_points: int
    level: int
    max_hp: int
    curr_hp: int
    fainted: bool
    in_hospital: bool
    owner: Optional[Trainer]
    curr_xp: int
    levelup_xp: int

    def __init__(
            self, name: str, pokemon_type: str, weakness: Dict[str, float],
            level: int, max_hp: int, attack_points: int, defense_points: int
    ) -> None:
        """Initialize this Pokemon, with the given name, type, weaknesses,
        level, health points, attack points, defense points and experience
        points.
        """
        super().__init__(
            name, pokemon_type, weakness, level, max_hp,
            attack_points, defense_points
        )
        self.curr_xp = 0
        self.levelup_xp = 100

    def attack(self, other: Pokemon) -> int:
        """Attack the other Pokemon and return the amount of damage inflicted.
        """
        attack_damage = max(self.attack_points - other.defense_points, 0) * 1.5
        attack_damage += random.random() * self.attack_points
        if self.type in other.weakness:
            attack_damage *= (1 + other.weakness[self.type])

        attack_damage = int(attack_damage)
        other.attacked(attack_damage)
        return attack_damage

    def attacked(self, attack_damage: int) -> None:
        """Change the current health points based on the amount of damage
        inflicted attack_damage.
        Pokemon faints if it has no health points.
        """
        self.curr_hp = max(0, self.curr_hp - attack_damage)
        if self.curr_hp == 0:
            self.fainted = True

    def add_xp(self, xp: int) -> bool:
        """Add experience points for this Pokemon and level up if appropriate.
        """
        self.curr_xp += xp
        if self.curr_xp >= self.levelup_xp:
            self.level += 1
            self.max_hp += 10
            self.attack_points += 1
            self.defense_points += 1
            self.curr_xp = self.curr_xp - self.levelup_xp
            self.levelup_xp = int(self.levelup_xp * 1.2)
            return True
        return False

    @classmethod
    def from_parent_class(cls, pokemon: poke.Pokemon) -> Pokemon:
        """Given an instance of the parent class, return the corresponding
        full-representation Pokemon.
        """
        new_pokemon = cls(
            pokemon.name, pokemon.type, pokemon.weakness,
            pokemon.level, pokemon.max_hp, pokemon.attack_points,
            pokemon.defense_points
        )
        new_pokemon.curr_hp = pokemon.curr_hp
        new_pokemon.fainted = pokemon.fainted
        new_pokemon.in_hospital = pokemon.in_hospital
        new_pokemon.owner = pokemon.owner
        return new_pokemon


class Trainer(poke.Trainer):
    """A more complete representation of a Pokemon trainer."""
    name: str
    level: int
    num_pokeballs: int
    coins: int
    curr_xp: int
    levelup_xp: int
    _all_pokemon: List[Pokemon]
    _battles: Dict[Trainer, Tuple[int, int]]

    def __init__(
            self, name: str, level: int = 1, num_pokeballs: int = 10,
            coins: int = 10
    ) -> None:
        """Initialize this Pokemon trainer, with the given name, level, number
        of pokeballs, coins and experience points.
        """
        super().__init__(
            name, level, num_pokeballs, coins
        )

        self.curr_xp = 0
        self.levelup_xp = 100

    def __str__(self) -> str:
        """Return a string representation of this Trainer.
        """
        res = f"TRAINER {self.name} | LVL {self.level} | XP {self.curr_xp}\n" \
              f"XP to next LVL: {self.levelup_xp - self.curr_xp}\n" \
              f"--------------------------\n" \
              f"\t{self.num_pokeballs} pokeballs\n" \
              f"\t{self.coins} coins\n" \
              f"\t{len(self._all_pokemon)} pokemon"

        win_rate = self.get_win_rate()
        if win_rate is None:
            res += "\n\t0 battles"
        else:
            res += f"\n\t{round(win_rate * 100, 1)}% battles won"
        return res

    @property
    def all_pokemon(self) -> List[Pokemon]:
        """Return all Pokemon collected by this Trainer.
        """
        return self._all_pokemon

    def get_available_pokemon(self) -> List[Pokemon]:
        """Return the list of Pokemon owned by this trainer that are neither
        fainted nor hospitalized.
        """
        result = []
        for pokemon in self._all_pokemon:
            if not pokemon.fainted and not pokemon.in_hospital:
                result.append(pokemon)
        return result

    def get_hospitalized_pokemon(self) -> List[Pokemon]:
        """Return the list of Pokemon owned by this trainer that are currently
        hospitalized.
        """
        return list(filter(
            lambda x: x.in_hospital, self._all_pokemon
        ))

    def get_non_hospitalized_pokemon(self) -> List[Pokemon]:
        """Return the list of Pokemon owned by this trainer that are currently
        not hospitalized.
        """
        return list(filter(
            lambda x: not x.in_hospital, self._all_pokemon
        ))

    def get_fainted_pokemon(self) -> List[Pokemon]:
        """Return a list of this Pokemon trainer's Pokemon that have fainted.
        """
        return list(filter(
            lambda x: x.fainted, self._all_pokemon
        ))

    def catch(self, pokemon: Pokemon) -> bool:
        """Return True iff the pokemon was caught.
        If caught, add pokemon to this Pokemon trainer's collection and update
        the Pokemon's owner.
        """
        is_caught = False
        if self.num_pokeballs > 0:
            success_rate = self.level / pokemon.level
            success_rate /= 1.5
            fail_rate = 1 - success_rate

            is_caught = random.choices(
                [True, False], [success_rate, fail_rate], k=1
            )

            if is_caught:
                self.add_pokemon(pokemon)
                self.num_pokeballs -= 1

        return is_caught

    def collect_coins(self, coins: int) -> None:
        """Update the number of coins owned by this Pokemon trainer.
        """
        self.coins += coins

    def add_xp(self, xp: int) -> bool:
        """Add amount experience points xp to this Pokemon Trainer.
        """
        self.curr_xp += xp
        if self.curr_xp >= self.levelup_xp:
            self.level += 1
            self.curr_xp = self.curr_xp - self.levelup_xp
            self.levelup_xp = int(self.levelup_xp * 1.2)
            return True
        return False

    def buy_pokeballs(self, num_pokeballs: int, pokeball_cost: int) -> int:
        """Buy the largest possible number of pokeballs that is at most
        num_pokeballs, each at the cost of pokeball_cost. Update the number of
        coins and number of pokeballs owned by this trainer accordingly and
        return the number of pokeballs bought.
        """
        afford_to_buy = num_pokeballs if pokeball_cost == 0 \
            else self.coins // pokeball_cost
        num_pokeballs = min(afford_to_buy, num_pokeballs)
        total_cost = num_pokeballs * pokeball_cost
        self.coins -= total_cost
        self.num_pokeballs += afford_to_buy
        return num_pokeballs

    @classmethod
    def from_parent_class(cls, trainer: poke.Trainer) -> Trainer:
        """Given an instance of the parent class, return the corresponding
        full-representation Pokemon trainer.
        """
        new_trainer = cls(
            trainer.name, trainer.level,
            trainer.num_pokeballs, trainer.coins
        )
        new_trainer._all_pokemon = trainer._all_pokemon
        new_trainer._battles = trainer._battles
        return new_trainer


class Battle:
    """A representation of a battle between the main player and an opponent
    """
    _player: Trainer
    _opponent: Trainer

    def __init__(
            self, main_player: Trainer, opponent: Trainer
    ) -> None:
        """Initialize this battle with the main_player against opponent.
        """
        self._player = main_player
        self._opponent = opponent

    def start(self) -> None:
        """Start this battle.
        """
        clear_screen()

        print(f"Battle: {self._player.name} Vs. {self._opponent.name}")
        print(
            f"Each player can use a maximum of {MAX_BATTLE_POKEMON} Pokemon."
        )

        if self._player.level < self._opponent.level:
            curr_player, curr_pokemon = self._player, None
            next_player, next_pokemon = self._opponent, None
        else:
            curr_player, curr_pokemon = self._opponent, None
            next_player, next_pokemon = self._player, None

        pokemon_used_so_far = {self._player: [], self._opponent: []}

        winner = None
        battle_ended = False
        while not battle_ended:

            if not curr_pokemon:
                curr_pokemon = self._choose_battle_pokemon(curr_player, None)
                pokemon_used_so_far[curr_player].append(curr_pokemon)
                print(f"{curr_player.name} chose {curr_pokemon.name}")

            if not next_pokemon:
                next_pokemon = self._choose_battle_pokemon(
                    next_player, curr_pokemon
                )
                pokemon_used_so_far[next_player].append(next_pokemon)
                print(f"{next_player.name} chose {next_pokemon.name}")

            attack_damage = curr_pokemon.attack(next_pokemon)
            print(self._get_attack_string(
                curr_pokemon, next_pokemon, attack_damage
            ))

            if curr_pokemon.fainted:
                print(f"{curr_player.name}'s {curr_pokemon.name} fainted.")
                curr_pokemon = None
                if next_pokemon.add_xp(10):
                    print(
                        f"{next_player.name}'s "
                        f"{next_pokemon.name} has levelled "
                        f"up to level {next_pokemon.level}"
                    )

            if next_pokemon.fainted:
                print(f"{next_player.name}'s {next_pokemon.name} fainted.")
                next_pokemon = None
                if curr_pokemon.add_xp(10):
                    print(
                        f"{next_player.name}'s {next_pokemon.name} has "
                        f"levelled up to level {next_pokemon.level}"
                    )

            time.sleep(1)

            both_players = [curr_player, next_player]
            for t_idx, trainer in enumerate(both_players):
                used_max_pokemon = len(list(filter(
                    lambda x: x.fainted, pokemon_used_so_far[trainer]
                ))) >= MAX_BATTLE_POKEMON
                no_more_pokemon = len(trainer.get_available_pokemon()) == 0
                battle_ended = used_max_pokemon or no_more_pokemon

                if used_max_pokemon:
                    print(
                        f"{trainer.name} used all {MAX_BATTLE_POKEMON} Pokemon."
                    )
                elif no_more_pokemon:
                    print(f"{trainer.name} has no more Pokemon.")

                if battle_ended:
                    winner = both_players[(t_idx + 1) % 2]

            curr_player, next_player = next_player, curr_player
            curr_pokemon, next_pokemon = next_pokemon, curr_pokemon

        loser = self._opponent if self._player == winner else self._player

        winner.record_battle_outcome(loser, True)
        if winner.add_xp(10):
            print(f"{winner.name} has levelled up to level {winner.level}")

        loser.record_battle_outcome(winner, False)

        print(f"Battle ended: {winner.name} won!")

    def _choose_battle_pokemon(
            self,
            curr_trainer: Trainer,
            opposing_pokemon: Optional[Pokemon] = None
    ) -> Pokemon:
        """Choose the Pokemon used in this battle.
        """

        selected_pokemon = None

        if curr_trainer == self._player:
            selected_pokemon = self.choose_pokemon()
        elif curr_trainer == self._opponent:
            selected_pokemon = self._opponent.choose_pokemon(opposing_pokemon)

        print(
            f"{curr_trainer.name} says: '{selected_pokemon.name}, "
            f"I choose you!'"
        )
        return selected_pokemon

    def choose_pokemon(self) -> Pokemon:
        """Return the Pokemon chosen by the user to participate in this battle.
        """
        print("Choose the Pokemon you want to send to battle.")
        return make_selection(self._player.get_available_pokemon())

    @staticmethod
    def _get_attack_string(
            attacker: Pokemon, attacked: Pokemon, attack_damage: int
    ) -> str:
        """Return a string representation of the attack by the attacker Pokemon
        on the attacked Pokemon, that resulted in attack_damage points.
        """
        if attack_damage > (0.5 * attacked.curr_hp):
            effective_str = "very"
            punctuation = "!"
        elif attack_damage > (0.3 * attacked.curr_hp):
            effective_str = "somewhat"
            punctuation = "."
        elif attack_damage == 0:
            effective_str = "not at all"
            punctuation = "..."
        else:
            effective_str = "not very"
            punctuation = "."
        return (
            f"\r{attacker.owner.name}'s {attacker.name} attacked "
            f"{attacked.owner.name}'s {attacked.name}. "
            f"It was {effective_str} effective{punctuation}\n"
        ) + (
            f"==========================================================\n"
            f"  {attacker.name:<13}  ||  {attacked.name:<13}  \n"
            f"==========================================================\n"
            f"  HP: {attacker.curr_hp:>4}/{attacker.max_hp:<4}  ||"
            f"  HP: {attacked.curr_hp:>4}/{attacked.max_hp:<4}  \n"
        )


class Game(poke.World):
    """A representation of a Pokemon Game.
    """
    _player: Trainer
    _trainers: List[Trainer]
    _pokemon: List[Pokemon]
    _pokecenters: List[poke.PokeCenter]
    _type_to_name_mapping: Dict[str, List[str]]
    _type_to_weakness_mapping: Dict[str, Dict[str, float]]
    _last_update: datetime
    actions: Dict[int, str]

    actions = {
        1: "Look around",
        2: "Challenge a trainer to a battle",
        3: "Manage inventory",
        4: "Your profile",
        5: "Pokedex",
        6: "Battle stats",
        7: "Visit Pokecenter",
        8: "Exit"
    }

    def __init__(self, player: Trainer):
        """Initialize this Pokemon Game
        """
        super().__init__(player)

        self._last_update = None

    def start(self) -> None:
        """Start this game.
        """
        self.setup()

        clear_screen()

        self._last_update = datetime.datetime.now()
        curr_action = 0
        while curr_action != 8:
            print("Select an option...")
            for k, v in self.actions.items():
                print(f"{k}: {v}")

            curr_action = input(">>> ").strip()
            curr_action = validate_input(
                curr_action, list(map(str, self.actions.keys()))
            )
            curr_action = int(curr_action)

            self.process_action(curr_action)

            clear_screen()

            if (datetime.datetime.now() - self._last_update).seconds >= 60:
                self.update()
                self._last_update = datetime.datetime.now()

        print(f"Goodbye, {self._player.name}!")

    def setup(self) -> None:
        """Populate this game with wild Pokemon, Trainers and Pokecenters.
        """
        print("Loading game data ...")

        with open('pokemon_data/pokemon_names.txt') as f_pokemon_types:
            self._type_to_name_mapping = \
                poke.load_pokemon_types(f_pokemon_types)

        with open('pokemon_data/pokemon_weaknesses.txt') as f_pokemon_weakness:
            self._type_to_weakness_mapping = \
                poke.load_pokemon_weakness(f_pokemon_weakness)

        with open('pokemon_data/pokemon_trainers.txt') as f_trainers:
            poke.load_trainers(f_trainers, self)

        self._modify_types()

        self.generate_wild_pokemon(INIT_NUM_WILD_POKEMON)

        self.generate_pokecenters(NUM_POKECENTERS)

        print("Game data loaded!")

    def update(self) -> None:
        """Update the status of this game to include more wild pokemon,
        heal sick Pokemon of trainers other than the main player, and heal
        Pokemon admitted in PokeCenters.
        """

        if len(self.get_wild_pokemon()) < 10:
            self.generate_wild_pokemon(UPDATE_NUM_WILD_POKEMON)

        # periodically, send other trainers' Pokemon to the Pokecenter
        self.admit_all_npc_pokemon(POKECENTER_TRAINER_LIMIT)

        for pokecenter in self._pokecenters:
            pokecenter.heal_admitted_pokemon()

        for trainer in self._trainers:
            if trainer != self._player:
                trainer_pokemon = trainer.get_hospitalized_pokemon()
                for pokemon in trainer_pokemon:
                    pokecenter = self.get_pokecenter_with_pokemon(pokemon)
                    trainer.request_pokecenter_discharge(pokemon, pokecenter)

    def generate_wild_pokemon(self, num_pokemon: int) -> None:
        """Generate wild Pokemon in this world.
        """

        name_types = set(self._type_to_name_mapping.keys())
        weakness_types = set(self._type_to_weakness_mapping.keys())
        pokemon_types = list(name_types.intersection(weakness_types))

        for _ in range(num_pokemon):

            pokemon_type = random.choice(pokemon_types)
            pokemon_name = random.choice(
                self._type_to_name_mapping[pokemon_type.lower()]
            )
            pokemon_weakness = self.get_pokemon_weakness(pokemon_type)

            pokemon_level = random.randint(
                max(1, self._player.level - 4), self._player.level * 2
            )
            pokemon_max_hp = random.randint(
                WILD_MIN_HP + 10 * pokemon_level,
                WILD_MAX_HP + 10 * pokemon_level
            )
            pokemon_atk = random.randint(WILD_MIN_ATK, WILD_MAX_ATK)
            pokemon_def = random.randint(WILD_MIN_DEF, WILD_MAX_DEF)

            new_pokemon = Pokemon(
                pokemon_name, pokemon_type, pokemon_weakness,
                1, pokemon_max_hp, pokemon_atk, pokemon_def
            )
            while new_pokemon.level != pokemon_level:
                new_pokemon.add_xp(new_pokemon.levelup_xp - new_pokemon.curr_xp)
            new_pokemon.curr_hp = new_pokemon.max_hp

            self.add_pokemon(new_pokemon)

    def generate_pokecenters(self, num_pokecenters: int) -> None:
        """Create Pokecenters in this world.
        """
        for p_idx in range(num_pokecenters):
            new_pokecenter = poke.PokeCenter(
                f"PC{p_idx + 1}",
                random.randint(MIN_POKECENTER_CAPACITY, MAX_POKECENTER_CAPACITY)
            )
            self.add_pokecenter(new_pokecenter)

    def process_action(self, action_code: int) -> None:
        """Respond to the user selection action_code.
        """
        action_function_mapping = {
            1: self.look_around,
            2: self.challenge_trainer,
            3: self.manage_inventory,
            4: self.view_profile,
            5: self.access_pokedex,
            6: self.view_battle_stats,
            7: self.visit_pokecenter
        }

        return action_function_mapping[action_code]() \
            if action_code in action_function_mapping else None

    def look_around(self) -> None:
        """Implement logic for action: Look around.
        """
        possibilities = {
            'find_pokemon': 4,
            'find_coins': 2,
            'nothing_happens': 3,
            'find_trainer': 1
        }
        event = random.choice([
            k for k, v in possibilities.items() for _ in range(v)
        ])

        if event == 'find_pokemon':
            all_wild_pokemon = self.get_wild_pokemon()
            if len(all_wild_pokemon) > 0:
                wild_pokemon = random.choice(all_wild_pokemon)

                print(f"A wild {wild_pokemon.name} has appeared!")
                print(wild_pokemon)

                if self._player.num_pokeballs <= 0:
                    print("Not enough pokeballs... You should go and buy some.")
                    return

                print(
                    f"You have {self._player.num_pokeballs} pokeballs. ",
                    f"Do you want to try to catch the wild {wild_pokemon.name}?"
                    f" [y/n]"
                )

                choice = input(">>> ").strip().lower()
                choice = validate_input(choice, ["y", "n"])
                if choice == "y":
                    pokemon_caught = self._player.catch(wild_pokemon)
                    if pokemon_caught:
                        print(f"{wild_pokemon.name} was successfully caught!")
                    else:
                        print(f"{wild_pokemon.name} escaped!")
                else:
                    print("You ran away!")
            else:
                print("You walk around for a bit... nothing exciting happens.")

        elif event == 'find_coins':

            num_coins = random.randint(1, max(self._player.coins // 5, 2))
            self._player.collect_coins(num_coins)
            print(
                f"You found {num_coins} coins! "
                f"You now have {self._player.coins} coins."
            )

        elif event == 'find_trainer':
            other_trainers_exist = any([
                (curr_trainer != self._player)
                and (len(curr_trainer.get_available_pokemon()) > 0)
                for curr_trainer in self._trainers
            ])

            if other_trainers_exist:
                trainer = None
                while not trainer or trainer == self._player \
                        or len(trainer.get_available_pokemon()) <= 0:
                    trainer = random.choice(self._trainers)

                print(
                    f"You bumped into {trainer.name}!",
                    "They challenge you to a battle"
                )

                if len(self._player.get_available_pokemon()) == 0:
                    print("You don't have any Pokemon to battle with ...")
                    choice = "n"
                else:
                    print(trainer)
                    print("Do you accept? [y/n]")
                    choice = input(">>> ").strip().lower()
                    choice = validate_input(choice, ["y", "n"])

                if choice == "y":
                    new_battle = Battle(self._player, trainer)
                    new_battle.start()
                else:
                    print(f"{self._player.name} ran away!")
            else:
                print("You walk around for a bit... nothing exciting happens.")

        else:
            print("You walk around for a bit... nothing exciting happens.")

        print("Press enter to exit.")
        input(">>> ")

    def challenge_trainer(self) -> None:
        """Implement logic for action: Challenge trainer.
        """
        available_trainers = [
            trainer for trainer in self._trainers
            if len(trainer.get_available_pokemon()) > 0
            and trainer != self._player
        ]

        if len(self._player.get_available_pokemon()) == 0:
            print("You don't have any Pokemon to battle with!")

            if len(self._player.get_all_pokemon()) == 0:
                print("Try exploring to catch some Pokemon.")
            elif len(self._player.get_fainted_pokemon()) > 0:
                print(
                    "Send some of your Pokemon to the Pokecenter so ",
                    "they can recover from battle."
                )
            elif len(self._player.get_hospitalized_pokemon()) > 0:
                print(
                    "You should retrieve some of your Pokemon from the ",
                    "pokecenter when they are healed."
                )
        elif len(available_trainers) > 0:
            # The player has at least one available _pokemon
            print("Choose a trainer to battle")
            opponent = make_selection(available_trainers)

            new_battle = Battle(self._player, opponent)
            new_battle.start()
        else:
            print("No trainers available to battle!")

        print("Press enter to exit.")
        input(">>> ")

    def manage_inventory(self) -> None:
        """Implement logic to action: Manage inventory.
        """
        print(
            f"You have {self._player.num_pokeballs} pokeballs. ",
            "Would you like to buy more? [y/n]"
        )

        choice = input(">>> ").strip().lower()
        choice = validate_input(choice, ["y", "n"])

        if choice == "y":
            max_purchase_num = self._player.coins // POKEBALL_COST

            if max_purchase_num < 1:
                print(
                    f"Not enough coins to buy pokeballs. "
                    f"You need at least {POKEBALL_COST} coins, "
                    f"but you only have {self._player.coins}."
                )
            else:
                print(
                    "How many pokeballs would you like to buy? "
                    f"(Max {max_purchase_num})"
                )
                choice = input(">>> ").strip()
                choice = int(validate_input(
                    choice,
                    list(map(str, range(1, max_purchase_num + 1)))
                ))

                num_bought = self._player.buy_pokeballs(choice, POKEBALL_COST)
                print(
                    f"You bought {num_bought} pokeballs. "
                    f"You now have {self._player.num_pokeballs} pokeballs.\n"
                    f"Your gold after the transaction: {self._player.coins}"
                )
        else:
            print("You left the shop without buying anything.")

        print("Press Enter to exit.")
        input(">>> ")

    def view_profile(self) -> None:
        """Implement logic to action: View profile.
        """
        print(self._player)

        if len(self._player.get_all_pokemon()) > 0:

            print("View Pokemon details? [y/n]")
            choice = input(">>> ").strip().lower()
            choice = validate_input(choice, ["y", "n"])

            if choice == "y":
                clear_screen()
                self._view_pokemon_details()
        else:
            print("No Pokemon to display ...")

        print("Press Enter to exit player profile.")
        input(">>> ")

    def access_pokedex(self) -> None:
        """Implement logic to action: Access Pokedex.
        """
        if len(self._player.get_all_pokemon()) > 0:
            self._view_pokemon_details()
        else:
            print("No Pokemon to display ...")

        print("Press Enter to exit player profile.")
        input(">>> ")

    def _view_pokemon_details(self) -> None:
        """Print the details of the Pokemon, selected by the user.
        """
        choice = "y"
        while choice == "y":

            print("Select Pokemon to view details")
            print(make_selection(
                self._player.get_all_pokemon(),
                lambda pokemon: pokemon.name
            ))

            print("View another Pokemon details? [y/n]")
            choice = input(">>> ").strip().lower()
            choice = validate_input(choice, ["y", "n"])

            clear_screen()

    def view_battle_stats(self) -> None:
        """Implement logic for action: Battle statistics.
        """
        print(f"BATTLE STATS\n{'-' * 55}")

        sorted_ranks = self.rank_trainers()
        if len(sorted_ranks) == 0:
            print("No Battles, yet. Try challenging a trainer to battle.")

        for r_idx, rank in enumerate(sorted_ranks):
            for trainer in rank:
                print(
                    f"[RANK {r_idx + 1:<3}] TRAINER {trainer.name:<10}"
                    f"\t\tWIN RATE: {trainer.get_win_rate() * 100}%"
                )
        print('-' * 55)
        print("Press enter to exit battle stats.")
        input(">>> ")

    def visit_pokecenter(self) -> None:
        """Implement the logic for the action: Visit pokecenter
        """
        print("Are you here to discharge or admit Pokemon?")

        choices = ["Admit Pokemon", "Discharge Pokemon", "Go Back"]
        for idx, elem in enumerate(choices):
            print(f"{idx + 1}: {elem}")

        choice = input(">>> ").strip()
        choice = int(validate_input(choice, ["1", "2", "3"]))

        while choice != 3:

            clear_screen()

            if choice == 1:
                self.send_to_pokecenter()
            else:
                self.discharge_from_pokecenter()

            print("What would you like to do next?")

            for idx, elem in enumerate(choices):
                print(f"{idx + 1}: {elem}")

            choice = input(">>> ").strip().lower()
            choice = int(validate_input(
                choice, [str(i + 1) for i in range(len(choices))]
            ))

        print("Press Enter to exit PokeCenter.")
        input(">>> ")

    def send_to_pokecenter(self) -> None:
        """Implement the logic for sending the selected Pokemon
        to the Pokecenter
        """

        if len(self._player.get_hospitalized_pokemon()) >= \
                len(self._player.get_all_pokemon()):
            print("all your Pokemon are already hospitalized")
            return

        done_selection = False
        while not done_selection:

            print("Select a pokecenter from the following: ")
            selected_pokecenter = self.select_available_pokecenter()

            print(
                f"Select Pokemon to send to Pokecenter {selected_pokecenter.id}"
            )

            pokemon_to_send = []
            remaining_pokemon = self._player.get_non_hospitalized_pokemon()
            choice = "y"
            while choice == "y" and selected_pokecenter.get_availability() > 0 \
                    and len(remaining_pokemon) > 0:

                print("Select Pokemon to send to pokecenter")
                pokemon = make_selection(
                    remaining_pokemon, lambda curr_pokemon: curr_pokemon.name
                )

                pokemon_to_send.append(pokemon)
                remaining_pokemon.remove(pokemon)

                if len(remaining_pokemon) > 0:

                    print(
                        f"Would you like to send another Pokemon to "
                        f"Pokecenter {selected_pokecenter.id}? [y/n]"
                    )

                    choice = input(">>> ").strip().lower()
                    choice = validate_input(choice, ["y", "n"])

            print(
                f"Sending {len(pokemon_to_send)} Pokemon to "
                f"Pokecenter {selected_pokecenter.id}"
            )

            for pokemon in pokemon_to_send:
                self._player.request_pokecenter_admission(
                    pokemon, selected_pokecenter
                )

            if len(self._player.get_hospitalized_pokemon()) == \
                    len(self._player.get_all_pokemon()):
                done_selection = True
            else:
                print("Do you want to select another PokeCenter? [y/n]")
                choice = input(">>> ").strip().lower()
                choice = validate_input(choice, ["y", "n"])
                done_selection = choice == "y"

        print("Press enter to exit.")
        input(">>> ")

    def get_pokecenter_with_pokemon(
            self, pokemon: Pokemon
    ) -> Optional[poke.PokeCenter]:
        """ Return the Pokecenter where pokemon is currently admitted.
        Return None if pokemon is not currently hospitalized.
        """
        for pokecenter in self._pokecenters:
            if pokecenter.is_admitted(pokemon):
                return pokecenter
        return None

    def select_available_pokecenter(self) -> poke.PokeCenter:
        """Return the Pokecenter selected by the user.
        """
        all_pokecenters = self.get_available_pokecenters()
        for p_idx, pokecenter in enumerate(all_pokecenters):
            print(f"{p_idx + 1}: {pokecenter.id}")

        choice = input(">>> ").strip()
        choice = int(validate_input(
            choice, [str(i + 1) for i in range(len(all_pokecenters))]
        ))

        selected_pokecenter = all_pokecenters[choice - 1]
        return selected_pokecenter

    def discharge_from_pokecenter(self) -> None:
        """Implement the logic for discharging the selected Pokemon
        from the Pokecenter.
        """
        if len(self._player.get_hospitalized_pokemon()) == 0:
            print("None of your Pokemon is hospitalized")
            return

        done_selection = False
        while not done_selection:

            print(
                "Which of your Pokemon would you like to discharge from "
                "the PokeCenter?"
            )

            selected_pokemon = make_selection(
                self._player.get_hospitalized_pokemon(),
                lambda pokemon: pokemon.name
            )
            pokecenter = self.get_pokecenter_with_pokemon(selected_pokemon)

            if not self._player.request_pokecenter_discharge(
                    selected_pokemon, pokecenter
            ):
                print(
                    f"Pokemon {selected_pokemon.name} "
                    f"is not ready to be discharged yet."
                )
            else:
                print(f"Pokemon {selected_pokemon.name} has been discharged")

            if len(self._player.get_hospitalized_pokemon()) == 0:
                done_selection = True
            else:
                print("Would you line to discharge another Pokemon? [y/n]")
                choice = input(">>> ").strip().lower()
                choice = validate_input(choice, ["y", "n"])
                done_selection = choice == "n"

        print("Press Enter key to exit")
        input(">>> ")

    def _modify_types(self) -> None:
        for t_idx, trainer in enumerate(self._trainers):
            if not isinstance(trainer, Trainer):
                self._trainers[t_idx] = Trainer.from_parent_class(trainer)
                trainer_pokemon = self._trainers[t_idx].all_pokemon

                for trainer_p_idx, pokemon in enumerate(trainer_pokemon):
                    if pokemon in self._pokemon:
                        w_idx = self._pokemon.index(pokemon)
                        self._pokemon[w_idx] = Pokemon.from_parent_class(
                            pokemon
                        )
                        trainer_pokemon[trainer_p_idx] = self._pokemon[w_idx]

        for p_idx, pokemon in enumerate(self._pokemon):
            if not isinstance(pokemon, Pokemon):
                self._pokemon[p_idx] = Pokemon.from_parent_class(pokemon)

    @classmethod
    def from_user_input(cls) -> Game:
        """Generate a new World using user input.
        """
        print("What is your name?")
        name = input(">>> ").strip()

        new_trainer = Trainer(name)

        print(f"Welcome, trainer {new_trainer.name}!")

        world = cls(new_trainer)
        return world


def make_selection(
        options: List[Any], repr_func: Optional[Callable] = None
) -> Any:
    """Present all options in options list to user, formatted using
    repr_function and return the selected choice.
    """
    for o_idx, option in enumerate(options):
        print(
            f"{o_idx + 1}: "
            f"{repr_func(option) if repr_func else option}"
        )

    choice = input(">>> ").strip()
    choice = int(validate_input(
        choice,
        [str(i + 1) for i in range(len(options))]
    ))

    return options[choice - 1]


def validate_input(choice: Any, valid_choices: List[Any]) -> bool:
    """Return True iff choice is in the list valid_choices.
    """
    while choice not in valid_choices:
        print("Invalid input.")
        choice = input(">>> ").strip().lower()
    return choice


def clear_screen() -> None:
    """Clear the screen
    """
    os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == '__main__':
    new_game = Game.from_user_input()
    new_game.start()
