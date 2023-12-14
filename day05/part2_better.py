"""
Day 5 part 2
https://adventofcode.com/2023/day/5#part2
"""
from pathlib import Path
from typing import Tuple, List

from day05.day5 import parse_input, NaiveWorkflow, Map, Workflow, Range

""" I let those commented out function as a remainder how I was thinking and trying to implement
a more efficient solution. 
"""
# def is_seed_range_behave_as_single_seed(seed_range: Tuple[int, int], wf: Workflow):
#     """ There is nothing there. """
#     first_seed = seed_range[0] + 0
#     last_seed = seed_range[0] + seed_range[1]
#     trace1 = []
#     trace2 = []
#     loc1 = wf.walk(first_seed, trace=trace1)
#     print(f"{first_seed=}: {loc1}")
#     loc2 = wf.walk(last_seed, trace=trace2)
#     print(f"{last_seed=}: {loc2}")
#     print(loc2 - loc1,  seed_range[1])
#
#     for t1, t2 in zip(trace1, trace2):
#         if t1[0] != t2[0] or t1[2] != t2[2]:
#             print(t1, t2)
#         else:
#             print(t1[0], t1[2], t1[1], t2[1])
#
#     return loc1 + seed_range[1] == loc2
#
#
# def can_we_squeeze_maps(seed_range: Tuple[int, int], wf: Workflow):
#     """
#     with this research function we can be sure that we can squeeze maps.
#
#     The goal is now to write a function that will cut the ranges of seeds in 3 blocks:
#         - the range before the overlap of the map
#         - the range in the overlap of the map
#         - the range after the overlap of the map
#
#     Each seed of those sub-ranges should go to the same location.
#     """
#     seed_range = range(seed_range[0], seed_range[0] + seed_range[1])
#     for m in wf.maps:
#         for r in m.ranges:
#             current_range = range(r.src_start, r.src_start + r.length)
#             intersection = range(max(seed_range.start, current_range.start), min(seed_range.stop, current_range.stop))
#             if len(intersection) > 0:
#                 print(f"Found intersection {current_range} and {seed_range}, intersection is {intersection}")
#                 break
#


def cut_range(seed_range: Tuple[int, int], wf: Workflow, name: str = None):
    seed_range = range(seed_range[0], seed_range[0] + seed_range[1] - 1)
    for m in wf.maps:
        if name is not None and m.name != name:
            continue
        for r in m.ranges:
            current_range = range(r.src_start, r.src_start + r.length - 1)
            intersection = range(max(seed_range.start, current_range.start), min(seed_range.stop, current_range.stop))
            if len(intersection) > 0:
                # print(f"Found intersection {current_range} and {seed_range}, intersection is {intersection}")
                if intersection.start == seed_range.start:
                    return (
                        (intersection.start, intersection.stop - intersection.start),
                        (intersection.stop, seed_range.stop - intersection.stop)
                    )
                elif intersection.stop == seed_range.stop:
                    return (
                        (seed_range.start, intersection.start - seed_range.start),
                        (intersection.start, intersection.stop - intersection.start),
                    )
                else:
                    return (
                        (seed_range.start, intersection.start - seed_range.start),
                        (intersection.start, intersection.stop - intersection.start),
                        (intersection.stop, seed_range.stop - intersection.stop),
                    )
    return (seed_range.start, seed_range.stop - seed_range.start),


def fine_cut_range(seed_range: Tuple[int, int], wf: Workflow):
    length = seed_range[1]
    seed_range_r = range(seed_range[0], seed_range[0] + length - 1)
    first = seed_range_r.start
    last = seed_range_r.stop

    for m in wf.maps:
        first_soil = m.get_destination(first)
        last_soil = m.get_destination(last)
        if last_soil - first_soil == length - 1:
            # Found no divergence at this level
            first = first_soil
            last = last_soil
            # print(f"{m.name} okay")
        else:
            # Need to cut here
            # print(f"{m.name}: {last_soil} - {first_soil} = {last_soil - first_soil} vs. {length}")
            new_ranges_of_layer_m = cut_range((first, last - first), wf, m.name)
            # Here we need to go back to the parent seeds
            # The start of the first range is the first seed
            # The end of the last range is the last seed
            # We just have to calculate the last seed of the first range, the first seed of the last range
            # should be that seed+1
            last_whatever_first_range = new_ranges_of_layer_m[0][0] + new_ranges_of_layer_m[0][1]
            skip = True
            for mm in wf.maps.__reversed__():
                if skip:
                    if mm.name == m.name:
                        skip = False
                    continue
                src = mm.get_source(last_whatever_first_range)
                last_whatever_first_range = src
            assert last_whatever_first_range in seed_range_r, (f"The calculated last seed {last_whatever_first_range} "
                                                               f"is not in seed range {seed_range_r}")
            first_sub_range_len = last_whatever_first_range - seed_range[0] + 1
            # Tracking the off-by-one problem
            if first_sub_range_len == 1:
                print(f"Range of one {seed_range[0]}, {first_sub_range_len}")
            return (seed_range[0], first_sub_range_len), (last_whatever_first_range + 1, seed_range[1] - first_sub_range_len)


def recursive_cut_seed_range(seed_range: Tuple[int, int], wf: Workflow) -> List[Tuple[int, int]]:
    result = []
    sr = fine_cut_range(seed_range, wf)
    if sr is None:
        result.append(seed_range)
    else:
        for r in sr:
            result.extend(recursive_cut_seed_range(r, wf))
    return result


def track_off_by_one(wf: Workflow, seed_to_check: int):
    """This function is used to track the off-by-one problem
    The passed-in seed is the seed to check against its predecessor and successor
    """
    traces = []
    source_dest = []
    for i in range(3):
        traces.append([])
        check = seed_to_check - 1 + i
        result = wf.walk(check, trace=traces[i])
        source_dest.append((check, result))
    for t in traces:
        print(t)

    prev = None
    for s, d in source_dest:
        print(f"Seed {s} --> Loc: {d}")
        if prev is not None:
            delta = d - prev
            if delta == 1:
                print("Off-by-one!")
        prev = d
    exit(0)


def better_part2(input_: str):
    seeds, maps = parse_input(input_)
    part_iter = seeds.part2_iter()
    # print(part_iter)
    wf = NaiveWorkflow(maps)

    # track_off_by_one(wf, 3435584797)
    # print(is_seed_range_behave_as_single_seed(seeds.part2_iter()[0], wf))
    # can_we_squeeze_maps(seeds.part2_iter()[0], wf)
    sub_ranges = []
    for i, seed_range in enumerate(part_iter):
        sub_ranges.extend(recursive_cut_seed_range(seed_range, wf))
        print(f"Loop #{i}: {sub_ranges}")
    print(len(sub_ranges))
    min_loc = 1e38
    for sr in sub_ranges:
        loc = wf.walk(sr[0])
        if loc < min_loc:
            min_loc = loc
    print(f"Solution of part #2: {min_loc} (minimum location)")


if __name__ == '__main__':
    import sys
    sys.setrecursionlimit(45000)
    sample = Path("part1.txt").read_text()
    better_part2(sample)
