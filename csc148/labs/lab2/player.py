from typing import List
import pytest
class Player:
    """A player

    ===Attributes==
    name: name of the player
    scores: list of scores from each match played by player

    ===Methods===
    Average: calculates the average points from n most recent matches

    >>> p1 = Player('Gesi')
    >>> p1.name
    'Gesi'
    >>> p1.scores
    []
    >>> p1.add_scrs([1, 2, 3, 4, 5])
    >>> p1.scores
    [1, 2, 3, 4, 5]
    >>> p1.scr_avg(3)
    4.0
    """

    def __init__(self, name: str):
        """"Initialise Player class
        >>> p1 = Player('Gesi')
        >>> p1.name
        'Gesi'
        >>> p1.scores
        []
        """
        self.name = name
        self.scores = []

    def add_scrs(self, scores: List[int]):
        """Add scores to Player
        >>> p1 = Player('Gesi')
        >>> p1.name
        'Gesi'
        >>> p1.scores
        []
        >>> p1.add_scrs([1, 2, 3, 4, 5])
        >>> p1.scores
        [1, 2, 3, 4, 5]
        """

        self.scores.extend(scores)

    def scr_avg(self, mst_rcnt: int):
        """Get average of mst_rcnt matches

        >>> p1 = Player('Gesi')
        >>> p1.name
        'Gesi'
        >>> p1.scores
        []
        >>> p1.add_scrs([1, 2, 3, 4, 5])
        >>> p1.scores
        [1, 2, 3, 4, 5]
        >>> p1.scr_avg(3)
        4.0
        """
        starting_point = len(self.scores) - mst_rcnt
        return sum(self.scores[starting_point :]) / mst_rcnt



if __name__ == '__main__':
    import doctest
    doctest.testmod()
