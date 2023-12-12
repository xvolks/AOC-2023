from enum import Enum
from pathlib import Path
from typing import List, Tuple

sample = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""

sample2 = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""


class Digits(Enum):
    """Correspondence table between digits and their values"""
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5
    six = 6
    seven = 7
    eight = 8
    nine = 9


def get_numbers_from_line(line: str) -> Tuple[int, int]:
    """
    gets the first and last digit of each line

    For example:
    :param line: `pqr3stu8vwx`
    :return: 3 and 8
    """
    left = -1
    right = -1
    for c in line:
        if c.isdigit():
            if left == -1:
                left = int(c)
                right = int(c)
            else:
                right = int(c)
    return left, right


def get_str_digits_from_line(line: str) -> Tuple[int, int]:
    """
    gets the first and last digit of each line,
    even if the digit is written as letters

    For example:
    :param line: `zoneight234`
    :return: 1 (one) and 4
    """
    left = -1
    right = -1
    for i, c in enumerate(line):
        for d in Digits:
            if line[i:].startswith(d.name):
                if left == -1:
                    left = d.value
                    right = d.value
                    break
                else:
                    right = d.value
                    break
        else:
            if c.isdigit():
                if left == -1:
                    left = int(c)
                    right = int(c)
                else:
                    right = int(c)
    return left, right


def calculate_sum(calibration_document: List[str], fn: callable = get_numbers_from_line) -> int:
    """
    For each line in the document:
    - get the first and last digit
    - glue them together to create a 2-digit number

    Sum all those numbers.
    :param calibration_document: the whole document as a list of strings
    :param fn: the function to extract the 1st and last digit depending if running for part1 or part2
    :return: the sum, result of the puzzle
    """
    total_sum = 0
    for line in calibration_document:
        calibration_value = fn(line)
        calibration_value = calibration_value[0] * 10 + calibration_value[1]
        total_sum += calibration_value
    return total_sum


def part1():
    sample = Path("day1-part1.txt").read_text()
    print(f"Result of part 1 is {calculate_sum(sample.splitlines())}")


def part2():
    sample = Path("day1-part1.txt").read_text()
    print(f"Result of part 2 is {calculate_sum(sample.splitlines(), fn=get_str_digits_from_line)}")


if __name__ == '__main__':
    print(f"Result of the sample for part1 is {calculate_sum(sample.splitlines())}")
    part1()
    print(f"Result of the sample for part2 is {calculate_sum(sample2.splitlines(), fn=get_str_digits_from_line)}")
    part2()
