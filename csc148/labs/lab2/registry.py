from __future__ import annotations
from typing import Dict, List

class Runner:
    """ A Runner
    ===Attributes===
    name: the first name of the player
    email: the email address of the player
    speed_cat: the speed category of the player

    ===Private Methods===
    _change_email: change the email address of the runner
    _change_speed: change the speed category of the runner

    >>> r1 = Runner('Fidel', 'fidel.widel@gmail.com', '<40')
    >>> r1.name
    'Fidel'
    >>> r1.speed_cat
    '<40'
    >>> r1._change_email('fidel_deboss@yahoo.com')
    >>> r1.email
    'fidel_deboss@yahoo.com'
    >>> r1._change_speed('<30')
    >>> r1.speed_cat
    '<30'
    """
    name: str
    email: str
    speed_cat: str

    def __init__(self, name: str, email: str, speed_cat: str):
        """Initialize class Runner
        >>> r1 = Runner('Fidel', 'fidel.widel@gmail.com', '<40')
        >>> r1.name
        'Fidel'
        >>> r1.speed_cat
        '<40'
        >>> r1.email
        'fidel.widel@gmail.com'
        """

        self.name = name
        self.email = email
        self.speed_cat = speed_cat

    def _change_email(self, new_email: str):
        """Change the Runner's email address
        >>> r1 = Runner('Fidel', 'fidel.widel@gmail.com', '<40')
        >>> r1.email
        'fidel.widel@gmail.com'
        >>> r1._change_email('fidel_deboss@yahoo.com')
        >>> r1.email
        'fidel_deboss@yahoo.com'
        """
        self.email = new_email

    def _change_speed(self, new_speed: str):
        """ Change the Player speed_category
        >>> r1 = Runner('Fidel', 'fidel.widel@gmail.com', '<40')
        >>> r1.speed_cat
        '<40'
        >>> r1._change_speed('<30')
        >>> r1.speed_cat
        '<30'
        """
        self.speed_cat = new_speed

    def __str__(self):
        """Return Runner as a string
        >>> r1 = Runner('Fidel', 'fidel.widel@gmail.com', '<40')
        >>> print(r1)
        Fidel, fidel.widel@gmail.com, <40
        """
        return self.name + ',' + ' ' + self.email + ',' + ' ' + self.speed_cat

class Registry:
    """A Registry
    ===Attributes===
    _id_ : the unique identifier of each runner, given in the order they
          registered, starting from 0
    _id_count : the place holder for the most recent id_ given
    reg_runners : dictionary of registered runners, with the id_ as the key,
                  and Runner as the value

    ===Methods===
    get_runners_by_speed: returns a list of runners in the same speed_category
    add_runner: adds runner to Registry, and assigns Runner instance an id_
    get_runner: returns the runner with the given id_
    get_runner_speed: returns the speed of the runner with the given id_
    withdraw: removes runner from registry
    change_email: changes the email address of runner with the given id_
    change_speed: changes the speed_category of runner with the given id_

    ===Representation Invariants===
    = _id_ >= 0
    = _id_count always starts at -1

    ===How it Works!===
    >>> olympics = Registry()
    >>> olympics.add_runner(Runner('Fidel', 'fidel.widel@gmail.com', '<40'))
    >>> olympics.reg_runners
    {0: 'Fidel, fidel.widel@gmail.com, <40'}
    >>> olympics.add_runner(Runner('Jayden', 'jayden_dayden@gmail.com', '<30'))
    >>> olympics.reg_runners
    {0: 'Fidel, fidel.widel@gmail.com, <40', 1: \
    'Jayden, jayden_dayden@gmail.com, <30'}
    >>> olympics.add_runner(Runner('Jessica', 'jessica_igot@gmail.com', '<20'))
    >>> olympics.add_runner(Runner('Intense', 'intense_mense@gmail.com', '<30'))
    >>> olympics.change_speed(0, '<30')
    {0: 'Fidel, fidel.widel@gmail.com, <30',\
    1: 'Jayden, jayden_dayden@gmail.com, <30',\
    2: 'Jessica, jessica_igot@gmail.com, <20',\
    3: 'Intense, intense_mense@gmail.com, <30'}
    """
    id_count: int
    reg_runners: Dict[int, Runner]

    def __init__(self):
        """Initialise class Register
        >>> olympics = Registry()
        >>> olympics.reg_runners
        {}
        >>> olympics.id_count
        -1
        """
        self.reg_runners = {}
        self.id_count = -1

    def add_runner(self, runner: Runner):
        """Add a runner to the registry and assign him/her/they an id
        >>> olympics = Registry()
        >>> olympics.add_runner(Runner('Fidel', 'fidel.widel@gmail.com', '<40'))
        >>> print(olympics)
        {0: 'Fidel, fidel.widel@gmail.com, <40'}
        """
        self.id_count += 1
        self.reg_runners[self.id_count] = runner

    def __str__(self):
        """Return a string representation of the registry
        >>> olympics = Registry()
        >>> olympics.add_runner(Runner('Fidel', 'fidel.widel@gmail.com', '<40'))
        >>> print(olympics)
        {0: 'Fidel, fidel.widel@gmail.com, <40'}
        """
        return "{" + "{}: \'{}, {}, {}\'".format(self.) + '}'

    def get_runner(self, id_: int):
        """Return a string representation of the runner with id <id_>
        >>> olympics = Registry()
        >>> olympics.add_runner(Runner('Fidel', 'fidel.widel@gmail.com', '<40'))
        >>> olympics.reg_runners
        {0: 'Fidel, fidel.widel@gmail.com, <40'}
        >>> olympics.get_runner(0)
        'Fidel, fidel.widel@gmail.com, <40'
        """
        return self.reg_runners[id_]

    def get_runner_speed(self, id_: int):
        """Return the speed category of the runner with id <id_>
        >>> olympics = Registry()
        >>> olympics.add_runner(Runner('Fidel', 'fidel.widel@gmail.com', '<40'))
        >>> olympics.reg_runners
        {0: 'Fidel, fidel.widel@gmail.com, <40'}
        >>> olympics.get_runner_speed(0)
        '<40'
        """
        speed = self.reg_runners[id_]
        return str(speed.speed_cat)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
