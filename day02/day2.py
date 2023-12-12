"""
Get story at : https://adventofcode.com/2023/day/2
"""
from dataclasses import dataclass
from pathlib import Path

sample = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""


@dataclass
class Cubes:
    """ This class represents the cubes drawn from the bag in the game."""
    red: int = 0
    blue: int = 0
    green: int = 0

    def add_round(self, cube_list: str):
        """
        Each round is provided with a list of cubes drawn from the bag.
        like this :
        Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
        A previous step has isolated each round in the form of a list of cubes:
         3 blue, 4 red

        In this example, there is no green cube, so we will initialize all variables to zero.

        This round will be compared with the current state of the cubes, and only the cubes that
        have a greater count will be counted.
        """
        # initialize all variables to zero
        r, g, b = 0, 0, 0
        cubes = cube_list.split(",")
        # count the cubes for each color
        for c in cubes:
            n, color = c.strip().split(" ")
            n = int(n)
            if color == "red":
                r = n
            elif color == "blue":
                b = n
            elif color == "green":
                g = n
        self.red = max(self.red, r)
        self.blue = max(self.blue, b)
        self.green = max(self.green, g)

    def is_possible(self):
        """
        The Elf would first like to know which games would have been possible if the bag contained only
        12 red cubes, 13 green cubes, and 14 blue cubes?
        """
        return self.red <= 12 and self.green <= 13 and self.blue <= 14

    def power(self) -> int:
        """
        The power of a set of cubes is equal to the numbers of red, green, and blue cubes multiplied together.
        For some reason it implied that if there are no cube for a color, it should be used in the multiplication.
        I'm not sure that case exists in the sample data.
        """
        # First ensure that there is at least one cube of each color, else the multiplication is zero
        if self.red == 0:
            self.red = 1
        if self.blue == 0:
            self.blue = 1
        if self.green == 0:
            self.green = 1

        # Now do the multiplication
        return self.red * self.green * self.blue


def part1(input_str: str):
    """
    Solve part 1 of the puzzle.
    - reading each line
    - parsing the game number
    - parsing the rounds
    - checking if the game is possible
    - summing up all the games that are possible
    """
    sum_ = 0
    for line in input_str.splitlines():
        game, line = line.split(":")
        _, g_num = game.strip().split(" ")
        g_num = int(g_num)
        cubes = Cubes()
        for round_ in line.split(";"):
            cubes.add_round(round_)
        if cubes.is_possible():
            # print(f"Game {g_num} is possible")
            sum_ += g_num
        else:
            # print(f"Game {g_num} is not possible")
            pass
    print(f"Solution of part #1 is {sum_}")


def part2(input_str: str):
    """
    Solve part 2 of the puzzle.
    - reading each line
    - parsing the game number
    - parsing the rounds
    - computing the power of the cubes
    - summing up all powers
    """
    sum_ = 0
    for line in input_str.splitlines():
        game, line = line.split(":")
        cubes = Cubes()
        for round_ in line.split(";"):
            cubes.add_round(round_)
        # print(cubes)
        power = cubes.power()
        sum_ += power
    print(f"Solution of part #2 is {sum_}")


if __name__ == '__main__':
    sample = Path("part1.txt").read_text()
    part1(sample)
    part2(sample)