from collections import Counter, OrderedDict
from dataclasses import dataclass
from enum import Enum, auto
from functools import cmp_to_key
from pathlib import Path
from typing import List, Dict, Optional

sample = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""

corner_cases = """33332 0
2AAAA 0
77888 0
77788 0"""


@dataclass
class HandPart1:
    hand: str
    bid: int
    rank: Optional["TypedHand"] = None

    RANK_ORDER = "AKQJT98765432"

    @classmethod
    def from_line(cls, line: str):
        h, b = line.split()
        return cls(h, int(b))

    def count_same_cards(self) -> Dict[str, int]:
        c = Counter(self.hand)
        return c

    def assign_rank(self):
        self.rank = TypedHand.from_hand(self)


@dataclass
class HandPart2:
    hand: str
    bid: int
    rank: Optional["TypedHand"] = None

    RANK_ORDER = "AKQT98765432J"

    @classmethod
    def from_line(cls, line: str):
        h, b = line.split()
        return cls(h, int(b))

    def count_same_cards(self) -> Dict[str, int]:
        c = Counter(self.hand)
        if c.keys().__contains__("J"):
            others = OrderedDict(c)
            num_jokers = others.pop("J")
            others = others.items()
            others = sorted(others, key=lambda x: x[1], reverse=True)
            try:
                if num_jokers == 5:
                    others = [ ('A', 5) ]
                else:
                    others[0] = (others[0][0], others[0][1] + num_jokers)
            except IndexError:
                print(others)
            c = dict(others)

        return c

    def assign_rank(self):
        self.rank = TypedHand.from_hand(self)


Hand = HandPart2


class TypedHand(Enum):
    HIGH_CARD = auto()
    ONE_PAIR = auto()
    TWO_PAIR = auto()
    THREE_OF_A_KIND = auto()
    FULL_HOUSE = auto()
    FOUR_OF_A_KIND = auto()
    FIVE_OF_A_KIND = auto()

    @classmethod
    def from_hand(cls, hand: Hand):
        cards_and_count = hand.count_same_cards()
        if len(cards_and_count) == 1:
            return cls.FIVE_OF_A_KIND
        if len(cards_and_count) == 2:
            if any(map(lambda x: x == 4, cards_and_count.values())):
                return cls.FOUR_OF_A_KIND
            else:
                return cls.FULL_HOUSE
        if len(cards_and_count) == 3:
            if any(map(lambda x: x == 3, cards_and_count.values())):
                return cls.THREE_OF_A_KIND
            else:
                return cls.TWO_PAIR
        if len(cards_and_count) == 4:
            return cls.ONE_PAIR
        return cls.HIGH_CARD


def hand_sorter(hands: List[Hand], comparator) -> List[Hand]:
    return sorted(hands, key=cmp_to_key(comparator), reverse=False)


def parse_input(sample: List[str]) -> List[Hand]:
    hands = []
    for line in sample:
        hands.append(Hand.from_line(line))
    return hands


def part1(lines: List[str]):
    def comparator(h1: Hand, h2: Hand) -> int:
        if h1.rank.value > h2.rank.value:
            return 1
        elif h1.rank.value < h2.rank.value:
            return -1
        else:
            for i, c1 in enumerate(h1.hand):
                c1 = Hand.RANK_ORDER.index(c1)
                c2 = Hand.RANK_ORDER.index(h2.hand[i])
                if c1 > c2:
                    return -1
                elif c1 < c2:
                    return 1
            return 0

    hands = parse_input(lines)
    for h in hands:
        h.assign_rank()

    hands = hand_sorter(hands, comparator)
    cpt = 0
    for rank, h in enumerate(hands):
        cpt += (rank+1) * h.bid
    print(f"Solution of part 1 is {cpt}")


def part2(lines: List[str]):
    def comparator(h1: Hand, h2: Hand) -> int:
        if h1.rank.value > h2.rank.value:
            return 1
        elif h1.rank.value < h2.rank.value:
            return -1
        else:
            for i, c1 in enumerate(h1.hand):
                c1 = Hand.RANK_ORDER.index(c1)
                c2 = Hand.RANK_ORDER.index(h2.hand[i])
                if c1 > c2:
                    return -1
                elif c1 < c2:
                    return 1
            return 0

    hands = parse_input(lines)
    for h in hands:
        h.assign_rank()

    hands = hand_sorter(hands, comparator)
    cpt = 0
    for rank, h in enumerate(hands):
        cpt += (rank+1) * h.bid
    print(f"Solution of part 2 is {cpt}")


if __name__ == '__main__':
    # part1(corner_cases.splitlines())
    # part1(sample.splitlines())
    # part1(Path("part1.txt").read_text().splitlines())

    # part2(corner_cases.splitlines())
    part2(sample.splitlines())
    part2(Path("part1.txt").read_text().splitlines())