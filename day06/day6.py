from dataclasses import dataclass
from typing import List

sample = """Time:      7  15   30
Distance:  9  40  200
"""

part1_sample = """Time:        45     98     83     73
Distance:   295   1734   1278   1210
"""


@dataclass
class Race:
    duration: int
    record: int

    def compute_all(self) -> List[int]:
        result = []
        for i in range(1, self.duration):
            result.append((self.duration - i) * i)
        return result


def parse_input_part1(lines: str) -> List[Race]:
    result = []
    lines = lines.splitlines()
    times = lines[0].split(":")[1].strip().split()
    record = lines[1].split(":")[1].strip().split()
    for t, r in zip(times, record):
        result.append(Race(int(t), int(r)))
    return result


def parse_input_part2(lines: str) -> Race:
    lines = lines.splitlines()
    times = lines[0].split(":")[1].replace(" ", "")
    record = lines[1].split(":")[1].replace(" ", "")
    return Race(int(times), int(record))


def part1(races: List[Race]):
    combinations = None
    for race in races:
        print(race)
        all_possible_outcomes = race.compute_all()
        record_beating = filter(lambda x: x > race.record, all_possible_outcomes)
        comb = len(list(record_beating))
        if combinations is None:
            combinations = comb
        else:
            combinations *= comb
    print(f"Solution of part 1 is {combinations}")


def part2(race: Race):
    all_possible_outcomes = race.compute_all()
    record_beating = filter(lambda x: x > race.record, all_possible_outcomes)
    print(f"Solution of part 2 is {len(list(record_beating))}")


if __name__ == '__main__':
    # part1(parse_input_part1(part1_sample))
    part2(parse_input_part2(part1_sample))