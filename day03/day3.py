"""
Get story at : https://adventofcode.com/2023/day/3
"""
from dataclasses import dataclass
from pathlib import Path
from typing import List, Iterator, Self

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


@dataclass
class PartNumber:
    """
    This is mostly a part of the blueprint as described in the problem.

    I've mixed the symbols with the part numbers in the representation.
    So an instance of this class represents either:
        - a part number
        - a symbol

    The fields are:
        value: the part number really described.
        symbol: it's not a part number, but a symbol
        x: position in the blueprint
        y: position in the blueprint
        l: length of the part number in characters (123 is 3 characters long)

    """
    value: int
    symbol: str
    x: int
    y: int
    l: int

    @classmethod
    def from_line(cls, line: str, num_line: int) -> Iterator[Self]:
        """
        Parse all the part numbers in the line
        :param line: something like `467..114..`
        :return: a generator of the part numbers
        """
        start = -1
        string = ""
        len_ = 0
        for i, c in enumerate(line):
            if c.isdigit():
                # we have a part number currently parsing
                if start == -1:
                    start = i
                string += c
                len_ += 1
            else:
                if start != -1:
                    # we have a part number finished parsing, yield it
                    yield cls(int(string), "", start, num_line, len_)
                start = -1
                string = ""
                len_ = 0
                if c != '.':
                    # we have a symbol, as it is a mono-character, yield it
                    yield cls(-1, c, i, num_line, 1)
        if start != -1:
            # we have a part number finished parsing because we reached the end of line, yield it
            yield cls(int(string), "", start, num_line, len_)


@dataclass
class EngineBluePrint:
    """
    This class represents the blueprint as described in the problem.
    It contains a list of part numbers and symbols.
    """
    values: List[PartNumber]

    def remove_isolated_num_from_symbol(self):
        """
        There are lots of numbers and symbols you don't really understand, but apparently any number adjacent to a
        symbol, even diagonally, is a "part number" and should be included in your sum.
        (Periods (.) do not count as a symbol.)

        So here we remove all the isolated numbers from the symbols.

        We just :
            - iterate over all the part numbers
            - if the part number has a symbol neighbor, we don't remove it
            - if the part number has no symbol neighbor, we remove it
        """
        to_remove = []
        for pn in self.values:
            if pn.value >= 0:
                if self.has_symbol_neighbors(pn):
                    # print(pn.value)
                    pass
                else:
                    # print(f"We should remove {pn.value}")
                    to_remove.append(pn)
        for pn in to_remove:
            pn.value = 0
            # self.values.remove(pn)

    def has_symbol_neighbors(self, pn: PartNumber) -> bool:
        """
        Checks if a given PartNumber object has any neighboring symbols.
        It iterates over a collection of n values and checks if the x and y coordinates of n fall within a range
        defined by start_x, end_x, start_y, and end_y.
        If a neighboring symbol is found, it returns True.
        If no neighboring symbols are found, it returns False.
        """
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
                    # print(f"{pn} has neighbor {n}")
                    return True
        return False

    def get_neighbor_values(self, n: PartNumber) -> List[PartNumber]:
        """
        Returns a list of part symbols that are neighbors of the given part number.
        """
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
        """
        Returns the sum of all the part numbers.
        Filters out the symbols part (that have a negative value)
        """
        return sum(map(lambda x: x.value if x.value >= 0 else 0, self.values))

    def print_with_blanks(self) -> str:
        """
        This is a debugging function that prints the blueprint after parsing it.

        I had a bug in my code that forgot to parse the numbers at the end of lines (two last lines
        in `PartNumber.from_string`)

        With this visualization and diff tool, I was able to spot the problem.

        The code is a bit messy, I let the reader improve it, and post a PR if needed.
        """
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
        """
        Returns the gear ratios of the engine.
        Filters out the symbols part (that have a negative value)

        The gear ratio is the product of the two neighboring part numbers separated by a symbol.
        """
        gear_ratios = []
        candidates = filter(lambda x: x.value < 0, self.values)
        for candidate in candidates:
            part_list = self.get_neighbor_values(candidate)
            if len(part_list) == 2:
                gear_ratios.append(part_list[0].value * part_list[1].value)

        return gear_ratios


def parse(lines: List[str]):
    """
    Parse the lines of the blueprint.
        - parse the part numbers
        - remove the isolated part numbers
        - calculate the sum of the part numbers

    :param lines: the lines of the blueprint
    """
    engine = EngineBluePrint(values=[])
    for i, l in enumerate(lines):
        pns = list(PartNumber.from_line(l, i))
        engine.values.extend(pns)
    engine.remove_isolated_num_from_symbol()
    print(f"Solution of part #1 is {engine.part_sum()}")
    print(f"Solution of part #2 is {sum(engine.get_gears_ratio())}")


if __name__ == '__main__':
    sample = Path("part1.txt").read_text()
    parse(sample.splitlines())