"""
Below is a Tournament class that records game outcomes and reports statistics.

Read the docstring for Tournament and its methods.

Your tasks are listed below.
Note: record_game is not implemented yet, so you won't be able to run
      the sample usage until after task 4.

    1.  Look at the Sample usage in Tournament.
        A precondition is violated within the sample usage.
        Fix the sample usage so that no preconditions are violated.
        Only one line in the sample usage should be changed.

    2. For Task 1, did you need to know how the instance attributes worked
       in order to identify the violated precondition?
       Write your answer in the space labelled <your answer here>.
       The answer itself won't be graded, but we will check that you wrote
       an answer.


       <your answer here>
        No, I didn't. I just had to check through for the only precondition
        given in the whole code.

    3.  At the end of the sample usage, add another example that calls:
            t.team_stats

        Write down the expected value of t.team_stats.
        If you're unsure of what team_stats is, read the documentation about
        Tournament's attributes.

    4.  Implement the method record_game.
        We have included some comments to help guide you.
        At this point, you should be able to run the doctests.

    5.  test_multiple_teams() is a test case that should pass. There is no
        bug within it, but there is one within Tournament.__init__

        Find the bug in Tournament.__init__ and fix it.
        It may help to draw a memory model diagram to understand where the
        bug is.

Submit your code on MarkUs and run the automated self-test.
Your grade on the quiz will be based solely on the results of the self-test.
(i.e. if you pass all of the tests, you get full marks on the quiz.)
"""
import pytest
from typing import List, Dict


class Tournament:
    """A sports tournament.

    === Attributes ===
    teams:
        The names of the teams in this tournament.
    team_stats:
        The history of each team in this tournament. Each key is a team name,
        and each value stores the number of games played and the number won.

    === Sample usage ===
    >>> t = Tournament(['Team A', 'Team B', 'Team C'])
    >>> t.record_game('Team A', 'Team B', 10, 4)
    >>> t.record_game('Team A', 'Team C', 5, 1)
    >>> t.record_game('Team B', 'Team C', 2, 0)
    >>> t.team_stats['Team B']
    [2, 1]
    >>> t.team_stats
    {'Team A': [2, 2], 'Team B': [2, 1], 'Team C': [2, 0]}
    """
    # Attribute types
    teams: List[str]
    team_stats: Dict[str, List[int]]

    def __init__(self, teams: List[str]) -> None:
        """Initialize a new Tournament among the given teams.
        """
        self.team_stats = {}
        self.teams = []

        for team in teams:
            self.teams.append(team)

        for team in self.teams:
            self.team_stats[team] = [0, 0]

    def record_game(self, team1: str, team2: str,
                    score1: int, score2: int) -> None:
        """Record the fact that <team1> played <team2> with the given scores.

        <team1> scored <score1> and <team2> scored <score2> in this game.

        Precondition: team1 and team2 are both in this tournament.
        """
        # Recall that the values in team_stats are lists in the form
        # [# games played, # of wins]
        # And that the keys are the team names.

        # Record that a game has been played for both teams.

        # Record that a game was won for the team with a higher score.
        # If there is a tie, no win is recorded.

        self.team_stats[team1][0] += 1
        self.team_stats[team2][0] += 1
        if score1 > score2:
            self.team_stats[team1][1] += 1
        elif score1 < score2:
            self.team_stats[team2][1] += 1

def test_multiple_teams():
    """Test that we can use the same list to create multiple Tournaments."""
    teams = ['Team A', 'Team B']
    t1 = Tournament(teams)

    teams.append('Team C')
    t2 = Tournament(teams)

    assert 'Team A' in t1.teams
    assert 'Team B' in t1.teams
    assert 'Team C' not in t1.teams

    assert 'Team A' in t2.teams
    assert 'Team B' in t2.teams
    assert 'Team C' in t2.teams


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    pytest.main(['quiz2.py'])
