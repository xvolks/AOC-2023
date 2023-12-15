from pathlib import Path
from typing import List

import cv2
import numpy as np
from tqdm import tqdm

from day10.part1 import parse_input, Maze, Pipe, PipeType

sample1 = (""".F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
""", 8)


sample2 = ("""FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
""", 10)


def compute_enclosed_tiles(input_: List[str]) -> int:
    maze = parse_input(input_)
    image = maze.draw()
    # count_steps() flags each connected pipe as visited
    maze.count_steps()
    count = 0
    cpt = 0
    path = list(filter(lambda p: not p.visited, maze.pipes))
    print(f"Maze has {len(maze.pipes)} pipes")
    print(f"Maze has a path of {len(path)} pipes")
    for t in tqdm(path):
        cpt += 1
        if is_enclosed(t, maze, image):
            cv2.imshow("image", image)
            if 27 == cv2.waitKey(1):
                break
            count += 1
    print(f"Found {count} inner pipes out of {cpt} pipes")
    cv2.waitKey(0)
    return count


def is_enclosed(pipe: Pipe, maze: Maze, image: np.ndarray = None) -> bool:
    """
    Check if the pipe is enclosed with the rayon cutting the maze:
     - if the number of intersections is odd, the pipe is not enclosed,
     - if the number of intersections is even, the pipe is enclosed.
    """
    scale = 3
    # print(f"Checking if pipe {pipe} is enclosed")
    x, y = pipe.x, pipe.y
    num_intersect = 0
    for i in range(x):
        p = maze.get_pipe_at(i, y)
        if not p.visited:
            continue
        # print(f"Pipe {i} {y} is {p.pipe_type} {p}")
        if p.pipe_type in (PipeType.VERT, PipeType.TR, PipeType.TL, PipeType.START):
            num_intersect += 1

    is_inside_x = num_intersect & 1 == 1
    if is_inside_x and image is not None:
        x *= scale
        y *= scale
        image[y:y + scale, x:x + scale] = 255
    return is_inside_x


if __name__ == '__main__':
    # perform algo for sample1
    count1 = compute_enclosed_tiles(sample1[0].splitlines())
    assert count1 == sample1[1], f"Expected {sample1[1]}, got {count1}"

    # perform algo for sample2
    count2 = compute_enclosed_tiles(sample2[0].splitlines())
    assert count2 == sample2[1], f"Expected {sample2[1]}, got {count2}"

    # perform algo for input
    input_ = Path('part1.txt').read_text()
    count = compute_enclosed_tiles(input_.splitlines())
    print(f"Result of part 2 is {count}")