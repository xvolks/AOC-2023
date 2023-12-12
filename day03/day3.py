from dataclasses import dataclass
from pathlib import Path
from typing import List, Iterator

sample = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""

class PartNumber:
    pass


@dataclass
class PartNumber:
    value: int
    symbol: str
    x: int
    y: int
    l: int

    @classmethod
    def from_line(cls, line: str, num_line: int) -> Iterator[PartNumber]:
        start = -1
        string = ""
        len = 0
        for i, c in enumerate(line):
            if c.isdigit():
                if start == -1:
                    start = i
                string += c
                len += 1
            else:
                if start != -1:
                    yield cls(int(string), "", start, num_line, len)
                start = -1
                string = ""
                len = 0
                if c != '.':
                    yield cls(-1, c, i, num_line, 1)
        if start != -1:
            yield cls(int(string), "", start, num_line, len)
@dataclass
class EngineBluePrint:
    values: List[PartNumber]

    def remove_isolated_num_from_symbol(self):
        to_remove = []
        for pn in self.values:
            if pn.value >= 0:
                if self.has_symbol_neighbors(pn):
                    print(pn.value)
                else:
                    print(f"We should remove {pn.value}")
                    to_remove.append(pn)
        for pn in to_remove:
            pn.value = 0
            # self.values.remove(pn)

    def has_symbol_neighbors(self, pn: PartNumber) -> bool:
        # keep diagonals
        start_x = pn.x - 1
        end_x = pn.x + pn.l
        start_y = pn.y - 1
        end_y = pn.y + 1
        for n in self.values:
            if n.value >= 0:
                # We are not interested in numbers, only symbols
                continue
            if start_x <= n.x <= end_x:
                if start_y <= n.y <= end_y:
                    print(f"{pn} has neighbor {n}")
                    return True
        return False

    def get_neighbor_values(self, n: PartNumber) -> List[PartNumber]:
        result = []
        for pn in self.values:
            if pn.value <= 0:
                # We are not interested in symbols
                continue
            if pn.y - 1 <= n.y <= pn.y + 1:
                if pn.x - 1 <= n.x <= pn.x + pn.l:
                    result.append(pn)
        return result

    def part_sum(self) -> int:
        return sum(map(lambda x: x.value if x.value >= 0 else 0, self.values))

    def print_with_blanks(self) -> str:
        y = 0
        result = ""
        s = ""
        for pn in self.values:
            if pn.y > y:
                if len(s) < 140:
                    s += '.' * (140 - len(s))
                result += s
                result += '\n'
                y = pn.y
                s = ""
            s += "." * (pn.x - len(s))
            if pn.value > 0:
                s += str(pn.value)
            elif pn.value < 0:
                s += pn.symbol
            else:
                fill_blank = '.'
                # fill_blank = 'X'
                s += fill_blank * pn.l

        if len(s) < 140:
            s += '.' * (140 - len(s))
        result += s
        result += '\n'
        return result

    def get_gears_ratio(self) -> List[int]:
        gear_ratios = []
        candidates = filter(lambda x: x.value < 0, self.values)
        for candidate in candidates:
            l = self.get_neighbor_values(candidate)
            if len(l) == 2:
                gear_ratios.append(l[0].value * l[1].value)

        return gear_ratios


def parse(lines: List[str]):
    engine = EngineBluePrint(values = [])
    for i, l in enumerate(lines):
        pns = list(PartNumber.from_line(l, i))
        engine.values.extend(pns)
    engine.remove_isolated_num_from_symbol()
    print(engine.part_sum())
    print(sum(engine.get_gears_ratio()))


if __name__ == '__main__':
    sample = Path("part1.txt").read_text()
    parse(sample.splitlines())