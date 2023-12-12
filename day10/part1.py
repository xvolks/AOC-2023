from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Tuple, List

import cv2
import numpy as np

sample1 = """-L|F7
7S-7|
L|7||
-L-J|
L|-JF"""


class PipeType(Enum):
    TL = 'F'
    BL = 'L'
    BR = 'J'
    START = 'S'
    TR = '7'
    HORZ = '-'
    VERT = '|'
    NOP = '.'

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

    @classmethod
    def from_type(cls, x: int, y: int, pipe_type: PipeType):
        return cls(pipe_type, x, y, pipe_type.shape())


@dataclass
class Maze:
    pipes: List[Pipe]
    height: int
    width: int

    def draw(self):
        scale = 3
        image = np.zeros((self.height * scale, self.width * scale), dtype=np.uint8)
        entry = None
        for pipe in self.pipes:
            x = pipe.x * scale
            y = pipe.y * scale
            if pipe.pipe_type == PipeType.START:
                entry = (x, y)
            image[y:y + scale, x:x + scale] = 255 * np.reshape(pipe.shape, (3, 3))

        cv2.imshow('image', image)
        cv2.waitKey(0)
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        cv2.floodFill(image, None, entry, (0, 0, 255))
        cv2.imshow('image', image)
        cv2.imwrite('maze.jpeg', image)
        cv2.waitKey(0)

    def count_steps(self) -> int:
        """
        I am at the starting point
        I can move in any direction
        Look for neighbors to find one that I can move to (connected to me)
        Move to that neighbor and repeat
        :return: the number of steps to get back to the starting point
        """
        return 42


def parse_input(input: List[str]):
    pipes = []
    for y, line in enumerate(input):
        for x, char in enumerate(line):
            pipe_type = PipeType.from_char(char)
            pipe = Pipe.from_type(x, y, pipe_type)
            pipes.append(pipe)

    height = len(input)
    width = len(input[0])

    maze = Maze(pipes, height, width)
    maze.draw()
    maze.count_steps()


if __name__ == '__main__':
    sample1 = Path("part1.txt").read_text()
    parse_input(sample1.splitlines())
