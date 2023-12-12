import abc
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, Type

from tqdm import tqdm

sample = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""


@dataclass
class Range:
    dst_start: int
    src_start: int
    length: int


@dataclass
class Map:
    name: str
    ranges: List[Range]

    @classmethod
    def from_lines(cls, map_name: str, lines: List[str]) -> "Map":
        ranges = []
        for line in lines:
            dst_start, src_start, length = map(int, line.split())
            ranges.append(Range(dst_start, src_start, length))
        return cls(map_name, ranges)

    def get_destination(self, src: int) -> int:
        for r in self.ranges:
            if r.src_start <= src < r.src_start + r.length:
                return r.dst_start + src - r.src_start
        return src

    def get_source(self, dest: int) -> int:
        for r in self.ranges:
            if r.dst_start <= dest < r.dst_start + r.length:
                return r.src_start + dest - r.dst_start
        return dest


@dataclass
class Seeds:
    seeds: List[int]

    @classmethod
    def from_line(cls, line: str) -> "Seeds":
        seeds, data = line.split(":")
        return cls(list(map(lambda x: int(x.strip()) , data.strip().split())))

    def part2_iter(self) -> List[Tuple[int, int]]:
        ranges = []
        curr = None
        for s in self.seeds:
            if curr:
                ranges.append((curr, s))
                curr = None
            else:
                curr = s
        return ranges


@dataclass
class Workflow:
    maps: List[Map]

    @abc.abstractmethod
    def walk(self, seed: int) -> int:
        ...

    @abc.abstractmethod
    def solve_part1(self, seeds: Seeds) -> int:
        ...

    @abc.abstractmethod
    def solve_part2(self, seeds: Seeds) -> int:
        ...


class NaiveWorkflow(Workflow):
    def solve_part1(self, seeds: Seeds) -> int:
        m = 9999999999999999
        for seed in seeds.seeds:
            s = self.walk(seed)
            if s < m:
                m = s
        return m

    def solve_part2(self, seeds: Seeds) -> int:
        m = 9999999999999999
        cpt = 0
        for seed_start, length in seeds.part2_iter():
            for seed in tqdm(range(seed_start, seed_start + length)):
                cpt += 1
                s = self.walk(seed)
                if s < m:
                    m = s

    def walk(self, seed: int) -> int:
        s = seed
        for mp in self.maps:
            d = mp.get_destination(s)
            s = d
        return s


class ReverseWorkflow(Workflow):
    def solve_part1(self, seeds: Seeds) -> int:
        loc = 0
        while True:
            s = self.walk(loc)
            if s in seeds.seeds:
                return loc
            loc += 1

    def solve_part2(self, seeds: Seeds) -> int:
        for loc in tqdm(range(1_000_000, 1_000_000_000)):
            s = self.walk(loc)
            for start, length in seeds.part2_iter():
                if start <= s < start + length:
                    return loc
            # loc += 1

    def walk(self, loc: int) -> int:
        s = loc
        for mp in self.maps.__reversed__():
            d = mp.get_source(s)
            s = d
        return s


def parse_input(text: str) -> Tuple[Seeds, List[Map]]:
    lines = text.splitlines()
    import re
    regex = re.compile(r"(?P<name>[\w-]+) map:")
    map_name = None
    values = []
    result = []
    for line in lines:
        if not line.strip():
            continue

        if line.startswith("seeds:"):
            seeds = Seeds.from_line(line)
            continue
        match = regex.match(line)
        if match:
            if map_name:
                result.append(Map.from_lines(map_name, values))
            values = []
            map_name = match.group("name")
        else:
            values.append(line)
    if map_name:
        result.append(Map.from_lines(map_name, values))
    return seeds, result


def part1(wfc: Type[Workflow]):
    # sample = Path("part1.txt").read_text()
    seeds, maps = parse_input(sample)
    wf = wfc(maps)
    m = wf.solve_part1(seeds)
    print(f"Solution of part #1 is location {m}")


def part2(wfc: Type[Workflow]):
    sample = Path("part1.txt").read_text()
    seeds, maps = parse_input(sample)
    wf = wfc(maps)
    m = wf.solve_part2(seeds)
    print(f"Solution of part #2 is location {m}")


if __name__ == '__main__':
    part1(NaiveWorkflow)
    # part2(NaiveWorkflow)
    part2(ReverseWorkflow)
