from math import gcd
from pathlib import Path
from typing import List, Dict

from aoc.day8 import day8
from aoc.day8.day8 import parse_input


def lcm(a: int, b: int) -> int:
    if a > b:
        greater = a
    else:
        greater = b
    while True:
        if (greater % a == 0) and (greater % b == 0):
            lcm = greater
            break
        greater += 1
    return lcm


def fast_lcm(a: int, b: int) -> int:
    return abs(a * b) // gcd(a, b)


def part2(lines: List[str]):
    guide, table = parse_input(lines)

    list_of_start = []
    for k in table.nodes.keys():
        if k.endswith("A"):
            list_of_start.append(k)

    print(list_of_start)

    ppcm = 1
    for n in list_of_start:
        def cond(x: str) -> bool:
            return x.endswith('Z')
        value = guide.walk_path(table, n, end_condition=cond)
        ppcm = fast_lcm(ppcm, value)
        print(f"{n} = {value}, {ppcm}")


if __name__ == '__main__':
    # sample2 = day08.sample2
    sample2 = Path("part1.txt").read_text()
    part2(sample2.splitlines())
