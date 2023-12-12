from collections import OrderedDict
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, Dict, Callable, Iterable, Union

sample = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""

sample2 = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""


@dataclass
class Guide:
    path: str

    @classmethod
    def from_string(cls, line: str) -> "Guide":
        return cls(line.strip())

    def walk_path(self, table: "Table", start: str = "AAA", end_condition: Callable[[str], bool] = lambda x: x == "ZZZ", prev_iter: int = 0) -> int:
        current_pos: Node = table.nodes[start]
        i = 0
        for c in self.path:
            if c == "L":
                current_pos = current_pos.left
            elif c == "R":
                current_pos = current_pos.right
            else:
                raise ValueError(f"Invalid character: {c}")
            i += 1
            if end_condition(current_pos.name):
                try:
                    return prev_iter + i
                except TypeError as e:
                    print(prev_iter, i)
                    raise
        return self.walk_path(table, current_pos.name, end_condition=end_condition, prev_iter=prev_iter + i)

    def walk_paths(self, table: "Table", starts: List[Union[str, "Node"]], end_condition: Callable[[str|Iterable["Node"]], bool] = lambda x: x == "ZZZ", prev_iter: int = 0) -> int:
        if all(map(lambda x: type(x) == str, starts)):
            current_pos: List[Node] = list(map(lambda x: table.nodes[x], starts))
        else:
            current_pos: List[Node] = starts
        i = 0
        for c in self.path:
            if c == "L":
                current_pos = list(map(lambda x: x.left, current_pos))
            elif c == "R":
                current_pos = list(map(lambda x: x.right, current_pos))
            else:
                raise ValueError(f"Invalid character: {c}")
            i += 1
            if end_condition(current_pos):
                try:
                    return prev_iter + i
                except TypeError as e:
                    print(prev_iter, i)
                    raise
        return self.walk_paths(table, current_pos, end_condition=end_condition, prev_iter=prev_iter + i)


@dataclass
class Node:
    name: str
    left: Union[str, "Node"]
    right: Union[str, "Node"]

    @classmethod
    def from_string(cls, line: str) -> "Node":
        import re
        regex = re.compile(r"(\w+) = \((\w+), (\w+)\)")
        match = regex.match(line)
        if not match:
            raise ValueError(f"Invalid line: {line}")
        name = match.group(1)
        left = match.group(2)
        right = match.group(3)
        return cls(name, left, right)

@dataclass
class Table:
    nodes: OrderedDict[str, Node]


def parse_input(lines: List[str]) -> Tuple[Guide, Table]:
    guide = Guide.from_string(lines[0])

    nodes = []
    for line in lines[2:]:
        node = Node.from_string(line)
        nodes.append(node)

    nodes = rebuild_table(nodes)
    table = Table(nodes)
    return guide, table


def rebuild_table(nodes: List[Node]) -> OrderedDict[str, Node]:
    table = OrderedDict()
    for node in nodes:
        table[node.name] = node
    for node in nodes:
        left = table[node.left]
        right = table[node.right]
        node.left = left
        node.right = right

    return table


def part1(lines: List[str]):
    guide, table = parse_input(lines)
    # print(guide)
    # print(table)
    print(guide.walk_path(table))


def part2(lines: List[str]):
    """This implementation would probably work on a real language, where recursion is a thing"""
    guide, table = parse_input(lines)

    def end_condition(nodes: Iterable[Node]) -> bool:
        m = list(map(lambda x: x.name.endswith("Z"), nodes))
        return len(m) > 0 and all(m)

    list_of_start = []
    for k in table.nodes.keys():
        if k.endswith("A"):
            list_of_start.append(k)
    print(guide.walk_paths(table, list_of_start, end_condition=end_condition))


if __name__ == '__main__':
    sample = Path("part1.txt").read_text()
    # This thing crashes in debug mode, Python is dog shit!
    part1(sample.splitlines())

    # sample2 = Path("part1.txt").read_text()
    # part2(sample2.splitlines())