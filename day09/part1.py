from dataclasses import dataclass
from pathlib import Path
from typing import List, Callable

sample = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""


@dataclass
class Measures:
    data: list[int]

    def derive(self) -> "Measures":
        data = []
        prev = None
        for i in self.data:
            if prev is None:
                prev = i
                continue
            data.append(i - prev)
            prev = i
        return Measures(data)

    def is_final(self):
        return all(map(lambda x: x == 0, self.data))

    @staticmethod
    def backpropagate(measures: List["Measures"]) -> int:
        sum = 0
        for measures in reversed(measures):
            sum += measures.data[-1]
        return sum

    @staticmethod
    def backpropagate_from_begin(measures: List["Measures"]) -> int:
        """ Here the logic is reversed

        y 0 3 6 9 12 15
         x 3 3 3 3  3
          z 0 0 0 0

         z is always 0, and x must be 3 here to keep the identity
         x - 3 = z
         0 - y = x

         so:
          - x - 3 = 0 --> x = 3
          - -y = x --> y = -3

        to generalize:
        x[i-1][1] - x[i-1][0] = x[i][0]
        =>
        x[i-1][0] = x[i-1][1] - x[i][0]

        """
        prev = 0
        for measures in reversed(measures):
            prev = measures.data[0] - prev
        return prev

    @classmethod
    def from_line(cls, line: str) -> "Measures":
        return cls(list(map(int, line.split())))


def main(lines: List[str], num_part: int, part: Callable[[List[Measures]], int]) -> None:
    next_values = []
    for text in lines:
        measures = Measures.from_line(text)
        # print(measures)
        history = [measures]

        while not measures.is_final():
            measures = measures.derive()
            history.append(measures)
            # print(measures)
        next_values.append(part(history))

    solution = sum(next_values)
    if len(lines) == 3:
        if num_part == 1:
            assert solution == 114, f"Got {solution}, expected 114"
        elif num_part == 2:
            assert solution == 2, f"Got {solution}, expected 2"
        else:
            raise ValueError(f"Unknown part {num_part}")

    print(f"Solution of part {num_part} is {solution}")


def perform_part1(history: List[Measures]) -> int:
    return Measures.backpropagate(history)


def perform_part2(history: List[Measures]) -> int:
    return Measures.backpropagate_from_begin(history)


if __name__ == '__main__':
    sample = Path("part1.txt").read_text()
    main(sample.splitlines(), 1, perform_part1)
    main(sample.splitlines(), 2, perform_part2)