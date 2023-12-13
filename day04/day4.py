"""
Get story at : https://adventofcode.com/2023/day/4
"""
from dataclasses import dataclass
from pathlib import Path
from typing import List, Any, Self

sample = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""


@dataclass
class Card:
    """
    This represents a scratchcard

    Fields:
        name: the name of the card (eg. Card 1)
        num: the number of the card (eg. 1)
        win_nums: the winning numbers (eg. [41, 48, 83, 86, 17])
        my_nums: the numbers that have been drawn (eg. [83, 86, 6, 31, 17, 9, 48, 53])
    """
    name: str
    num: int
    win_nums: List[int]
    my_nums: List[int]

    def compute_points(self) -> int:
        """
        Compute the points for the card, the rule is : ``Card 1 has five winning numbers.
        Of the numbers you have, four of them are winning numbers! That means card 1 is worth 8 points (1 for the
        first match, then doubled three times for each of the three matches after the first).``

        So:

        - no wins-> 0 points
        - 1 win  -> 1 point
        - 2 wins -> 2 points
        - 3 wins -> 4 points
        - 4 wins -> 8 points

        `points = 1 << (wins - 1) if wins > 0 else 0`

         This is equivalent to the following code:

         `points = 2 ** (wins - 1) if wins > 0 else 0`

         where `**` operator is the power operator

        """
        count = self.compute_num_wins()
        if count == 0:
            return 0
        else:
            return 1 << (count - 1)

    def compute_num_wins(self) -> int:
        """
        Counts how many times the winning numbers appear in the my_nums
        """
        count = 0
        for win in self.win_nums:
            if win in self.my_nums:
                count += 1
        return count

    @classmethod
    def from_line(cls, line: str) -> Self:
        """
        Creates a card from a line of text like `Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53`

        - the first part is the name
        - the second part is the number of the card
        - the third part is the winning numbers
        - the fourth part is the numbers that have been drawn

        We start by splitting the line on the `:` separator, and then on the `|` separator, we are also splitting
        the word Card and the number of the card by default split function.


        :param line: the input line
        :return: the created card instance
        """
        card_name, data = line.split(":")
        _, c_num = card_name.split()

        winners, mines = data.strip().split("|")
        # split on spaces to get the numbers as strings and convert them to int using map, creating a list of ints
        winners = list(map(int, winners.strip().split()))
        mines = list(map(int, mines.strip().split()))

        return cls(card_name, int(c_num), winners, mines)


def duplicate_x_cards(deck: List[Card], num: int, count: int):
    """
    Duplicate cards in a range of x cards
    :param deck: the deck of cards
    :param num: the starting card number (excluded from the duplication)
    :param count: the number of cards to duplicate after that
    :return: the list of duplicated cards
    """
    dupli = []
    for i in range(count):
        dupli.append(deck[num + i])
    return dupli


def play_game(cards: List[Card]) -> List[Card]:
    """
    Play a game of bingo, hum, advent of code.

    This is a recursive function that will play the game until there are no more cards that can win.
    :param cards: the initial deck of cards for this round
    :return: the card won in this round
    """
    won_cards = []
    for card in cards:
        num_wins = card.compute_num_wins()
        if num_wins > 0:
            won_cards.extend(duplicate_x_cards(new_deck, card.num, num_wins))

    if len(won_cards) == 0:
        return []
    won_cards.extend(play_game(won_cards))
    return won_cards


if __name__ == '__main__':
    sample = Path("part1.txt").read_text()
    cards = []
    for l in sample.splitlines():
        card = Card.from_line(l)
        cards.append(card)
        # print(card, card.compute_win())

    # sums the points for each card
    print(f"Part 1 solution {sum(map(lambda x: x.compute_points(), cards))}")

    # part 2
    new_deck = [c for c in cards]
    won_cards = play_game(new_deck)
    new_deck.extend(won_cards)
    print(f"Part 2 solution {len(new_deck)}")