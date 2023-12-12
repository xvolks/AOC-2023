from dataclasses import dataclass
from pathlib import Path

sample_games = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""

@dataclass
class Cubes:
    red: int = 0
    blue: int = 0
    green: int = 0

    def add_round(self, cube_list: str):
        cubes = cube_list.split(",")
        r, g, b = 0, 0, 0

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
        return self.red <= 12 and self.green <= 13 and self.blue <= 14

    def power(self) -> int:
        if self.red == 0:
            self.red = 1
        if self.blue == 0:
            self.blue = 1
        if self.green == 0:
            self.green = 1
        return self.red * self.green * self.blue


def part1():
    games = {}
    sum = 0
    sample_games = Path("part1.txt").read_text()
    for line in sample_games.splitlines():
        game, line = line.split(":")
        _, g_num = game.strip().split(" ")
        g_num = int(g_num)
        cubes = Cubes()
        for round in line.split(";"):
            cubes.add_round(round)
        print(cubes)
        games[g_num] = cubes
        if cubes.is_possible():
            print(f"Game {g_num} is possible")
            sum += g_num
        else:
            print(f"Game {g_num} is not possible")
    print(sum)


def part2():
    games = {}
    sum = 0
    sample_games = Path("part1.txt").read_text()
    for line in sample_games.splitlines():
        game, line = line.split(":")
        _, g_num = game.strip().split(" ")
        g_num = int(g_num)
        cubes = Cubes()
        for round in line.split(";"):
            cubes.add_round(round)
        print(cubes)
        power = cubes.power()
        sum += power
    print(sum)


if __name__ == '__main__':
    # part1()
    part2()