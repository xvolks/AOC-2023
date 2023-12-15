"""
Get the story at https://adventofcode.com/2023/day/10
"""
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Tuple, List, Optional

import cv2
import numpy as np

sample1 = """-L|F7
7S-7|
L|7||
-L-J|
L|-JF"""


class Direction(Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3


class PipeType(Enum):
    TL = 'F'
    BL = 'L'
    BR = 'J'
    START = 'S'
    TR = '7'
    HORZ = '-'
    VERT = '|'
    NOP = '.'

    def possible_directions(self) -> Optional[Tuple[Direction, Direction]]:
        if self == PipeType.TL:
            return Direction.RIGHT, Direction.DOWN
        if self == PipeType.BL:
            return Direction.RIGHT, Direction.UP
        if self == PipeType.BR:
            return Direction.LEFT, Direction.UP
        if self == PipeType.TR:
            return Direction.LEFT, Direction.DOWN
        if self == PipeType.HORZ:
            return Direction.RIGHT, Direction.LEFT
        if self == PipeType.VERT:
            return Direction.UP, Direction.DOWN
        return None

    def shape(self) -> Tuple[int, int, int, int, int, int, int, int, int ]:
        if self == PipeType.TL:  # Top Left
            return 0, 0, 0, 0, 1, 1, 0, 1, 0
        if self == PipeType.BL:  # Bottom Left
            return 0, 1, 0, 0, 1, 1, 0, 0, 0
        if self == PipeType.BR:  # Bottom Right
            return 0, 1, 0, 1, 1, 0, 0, 0, 0
        if self == PipeType.TR:  # Top Right
            return 0, 0, 0, 1, 1, 0, 0, 1, 0
        if self == PipeType.HORZ:  # Horizontal
            return 0, 0, 0, 1, 1, 1, 0, 0, 0
        if self == PipeType.VERT:  # Vertical
            return 0, 1, 0, 0, 1, 0, 0, 1, 0
        if self == PipeType.NOP:  # No Pipe
            return 0, 0, 0, 0, 0, 0, 0, 0, 0
        if self == PipeType.START:  # Start
            return 1, 1, 1, 1, 1, 1, 1, 1, 1

    @classmethod
    def from_char(cls, char: str):
        for pipe_type in PipeType:
            if pipe_type.value == char:
                return pipe_type
        raise ValueError(f'Invalid char: {char}')


@dataclass
class Pipe:
    pipe_type: PipeType
    x: int
    y: int
    shape: Tuple[int, int, int, int, int, int, int, int, int]
    visited: bool = False

    @classmethod
    def from_type(cls, x: int, y: int, pipe_type: PipeType):
        return cls(pipe_type, x, y, pipe_type.shape())

    def can_go(self, direction: Direction) -> bool:
        if direction == Direction.RIGHT:
            return self.pipe_type == PipeType.HORZ or self.pipe_type == PipeType.TL or self.pipe_type == PipeType.BL
        if direction == Direction.LEFT:
            return self.pipe_type == PipeType.HORZ or self.pipe_type == PipeType.TR or self.pipe_type == PipeType.BR
        if direction == Direction.DOWN:
            return self.pipe_type == PipeType.VERT or self.pipe_type == PipeType.TL or self.pipe_type == PipeType.TR
        if direction == Direction.UP:
            return self.pipe_type == PipeType.VERT or self.pipe_type == PipeType.BL or self.pipe_type == PipeType.BR
        raise ValueError(f'Invalid direction: {direction}')

    def get_other_end_going_to(self, direction: Direction) -> Direction:
        """
        Here we are going to find the other end of the pipe
        after a movement in a certain `direction`,
        for example:
        .. code-block:: text
             +----+    F-7
             |    |    S |
             +----+    L-J

        Starting at S, we are going UP, so `direction` is UP.
        For F (the next pipe) we are coming from DOWN, and we need to return the next direction.

        The next direction for this Top Left corner is RIGHT obviously.

        """
        match direction:
            case Direction.RIGHT:
                coming_from = Direction.LEFT
            case Direction.LEFT:
                coming_from = Direction.RIGHT
            case Direction.UP:
                coming_from = Direction.DOWN
            case Direction.DOWN:
                coming_from = Direction.UP

        directions = self.pipe_type.possible_directions()
        if directions is None:
            raise ValueError(f'Invalid pipe type: {self.pipe_type}')
        next_directions = list(filter(lambda d: d != coming_from, directions))
        return next_directions[0]


@dataclass
class Maze:
    pipes: List[Pipe]
    height: int
    width: int
    _pipes_cache: List[List[Optional[Pipe]]] = None

    def draw(self) -> np.ndarray:
        scale = 3
        image = np.zeros((self.height * scale, self.width * scale), dtype=np.uint8)
        entry = None
        for pipe in self.pipes:
            x = pipe.x * scale
            y = pipe.y * scale
            if pipe.pipe_type == PipeType.START:
                entry = (x, y)
            if pipe.visited:
                mul = 255
            else:
                mul = 128
            image[y:y + scale, x:x + scale] = mul * np.reshape(pipe.shape, (3, 3))

        cv2.imshow('image', image)
        cv2.waitKey(0)
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        cv2.floodFill(image, None, entry, (0, 0, 255))
        cv2.imshow('image', image)
        cv2.imwrite('maze.jpeg', image)
        cv2.waitKey(0)
        return image

    def count_steps(self) -> int:
        """
        Search starting point in the maze
        I am at the starting point
        I can move in any direction
        Look for neighbors to find one that I can move to (connected to me)
        Move to that neighbor and repeat
        :return: the number of steps to get back to the starting point
        """
        if self._pipes_cache is None:
            self._pipes_cache = [[None for _ in range(self.height)] for _ in range(self.width)]
        starting_point = next(filter(lambda p: p.pipe_type == PipeType.START, self.pipes))

        # this is the first step
        current_pipe = self.get_next_pipe(starting_point)
        steps = 1

        prev = starting_point
        # Search whole pipe network until I reach back to the starting point
        while current_pipe.pipe_type != PipeType.START:
            next_pipe = self.get_next_possible_pipe(prev, current_pipe)
            prev = current_pipe
            current_pipe = next_pipe
            steps += 1

        return steps

    def get_next_possible_pipe(self, prev: Pipe, current_pipe: Pipe) -> Pipe:
        delta_x = current_pipe.x - prev.x
        delta_y = current_pipe.y - prev.y
        if delta_y == 0:
            # horizontal movement
            if delta_x > 0:
                # go right
                new_direction = current_pipe.get_other_end_going_to(Direction.RIGHT)
            else:
                # go left
                new_direction = current_pipe.get_other_end_going_to(Direction.LEFT)
        else:
            # vertical movement (the Y axis is oriented downwards)
            if delta_y > 0:
                # go down
                new_direction = current_pipe.get_other_end_going_to(Direction.DOWN)
            else:
                # go up
                new_direction = current_pipe.get_other_end_going_to(Direction.UP)
        next_step = self.get_neighbor_pipe(current_pipe, new_direction)
        next_step.visited = True
        return next_step

    def get_neighbor_pipe(self, pipe: Pipe, direction: Direction) -> Pipe:
        """
        Get the pipe next to `pipe` in the direction `direction`
        """
        x = pipe.x
        y = pipe.y
        if direction == Direction.RIGHT:
            x += 1
        elif direction == Direction.LEFT:
            x -= 1
        elif direction == Direction.DOWN:
            y += 1
        elif direction == Direction.UP:
            y -= 1
        else:
            raise ValueError(f'Invalid direction: {direction}')
        return self.get_pipe_at(x, y)

    def get_pipe_at(self, x: int, y: int) -> Pipe:
        _cache = self._pipes_cache[x][y]
        if _cache is None:
            _cache = next(filter(lambda p: p.x == x and p.y == y, self.pipes))
            self._pipes_cache[x][y] = _cache
        return _cache

    def get_next_pipe(self, starting_point: Pipe) -> Pipe:
        left = self.get_pipe_at(starting_point.x - 1, starting_point.y)
        if left.visited or not left.can_go(Direction.RIGHT):
            right = self.get_pipe_at(starting_point.x + 1, starting_point.y)
            if right.visited or not right.can_go(Direction.LEFT):
                up = self.get_pipe_at(starting_point.x, starting_point.y - 1)
                if up.visited or not up.can_go(Direction.DOWN):
                    down = self.get_pipe_at(starting_point.x, starting_point.y + 1)
                    if down.visited:
                        raise ValueError('Already visited')
                    next_point = down
                else:
                    next_point = up
            else:
                next_point = right
        else:
            next_point = left

        next_point.visited = True
        return next_point


def parse_input(input: List[str]) -> Maze:
    pipes = []
    for y, line in enumerate(input):
        for x, char in enumerate(line):
            pipe_type = PipeType.from_char(char)
            pipe = Pipe.from_type(x, y, pipe_type)
            pipes.append(pipe)

    height = len(input)
    width = len(input[0])

    return Maze(pipes, height, width)


def part1(maze: Maze):
    print(f"Solution of part #1 is {maze.count_steps() // 2}")


if __name__ == '__main__':
    sample1 = Path("part1.txt").read_text()
    maze = parse_input(sample1.splitlines())
    try:
        part1(maze)
    except ValueError as e:
        print(e)
    maze.draw()

