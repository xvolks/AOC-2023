from dataclasses import dataclass
from pathlib import Path
from typing import List, Any

sample = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""

@dataclass
class Card:
    name: str
    num: int
    win_nums: List[int]
    my_nums: List[int]

    def compute_points(self) -> int:
        count = self.compute_num_wins()
        if count == 0:
            return 0
        else:
            return 1 << (count - 1)

    def compute_num_wins(self) -> int:
        count = 0
        for win in self.win_nums:
            if win in self.my_nums:
                count += 1
        return count

    @classmethod
    def from_line(cls, line: str) -> Any:
        card_name, data = line.split(":")
        _, c_num = card_name.split()

        winners, mines = data.strip().split("|")
        winners = map(lambda x: int(x.strip()), filter(lambda x: len(x.strip()), winners.strip().split(" ")))
        mines = map(lambda x: int(x.strip()), filter(lambda x: len(x.strip()), mines.strip().split(" ")))

        return cls(card_name, int(c_num), list(winners), list(mines))


def duplicate_x_cards(deck: List[Card], num: int, count: int):
    dupli = []
    for i in range(count):
        dupli.append(deck[num + i])
    return dupli


def play_game(cards: List[Card]) -> List[Card]:
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

    print(f"Part 1 solution {sum(map(lambda x: x.compute_points(), cards))}")

    new_deck = [c for c in cards]
    won_cards = play_game(new_deck)
    new_deck.extend(won_cards)
    print(f"Part 2 solution {len(new_deck)}")