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
    seed_range = range(seed_range[0], seed_range[0] + seed_range[1])
    for m in wf.maps:
        if name is not None and m.name != name:
            continue
        for r in m.ranges:
            current_range = range(r.src_start, r.src_start + r.length)
            intersection = range(max(seed_range.start, current_range.start), min(seed_range.stop, current_range.stop))
            if len(intersection) > 0:
                # print(f"Found intersection {current_range} and {seed_range}, intersection is {intersection}")
                intersection_len = intersection.stop - intersection.start
                trailing_len = seed_range.stop - intersection.stop
                heading_len = intersection.start - seed_range.start
                if intersection.start == seed_range.start:
                    if trailing_len > 0:
                        return (
                            (intersection.start, intersection_len),
                            (intersection.stop, trailing_len)
                        )
                    else:
                        return (intersection.start, intersection_len),

                elif intersection.stop == seed_range.stop:
                    if heading_len > 0:
                        return (
                            (seed_range.start, heading_len),
                            (intersection.start, intersection_len),
                        )
                    else:
                        return (intersection.start, intersection_len),
                else:
                    return (
                        (seed_range.start, heading_len),
                        (intersection.start, intersection_len),
                        (intersection.stop, trailing_len),
                    )
    return (seed_range.start, seed_range.stop - seed_range.start),


def fine_cut_range(seed_range: Tuple[int, int], wf: Workflow):
    length = seed_range[1]
    seed_range_r = range(seed_range[0], seed_range[0] + length)
    first = seed_range_r.start
    last = seed_range_r.stop - 1

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
            new_ranges_of_layer_m = cut_range((first, length), wf, m.name)
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
            first_sub_range_len = last_whatever_first_range - seed_range[0]
            secnd_sub_range_len = seed_range[1] - first_sub_range_len
            # Tracking the off-by-one problem
            if first_sub_range_len == 2 or secnd_sub_range_len == 2:
                print(f"Range of one {seed_range[0]}, {first_sub_range_len}")

            return (seed_range[0], first_sub_range_len), (last_whatever_first_range, secnd_sub_range_len)


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


def reproduce_off_by_one(wf: Workflow, s_range: Tuple[int, int]):
    """This function is used to reproduce the off-by-one problem"""
    all_ranges = recursive_cut_seed_range(s_range, wf)
    for i, r in enumerate(all_ranges):
        print(f"New range #{i} : {r}")
        track_off_by_one(wf, r[0])
    exit(0)


def better_part2(input_: str):
    seeds, maps = parse_input(input_)
    part_iter = seeds.part2_iter()
    # print(part_iter)
    wf = NaiveWorkflow(maps)
    import time
    start = time.time()
    # reproduce_off_by_one(wf, (1808166864, 294882110))
    # track_off_by_one(wf, 1866167533)
    # print(is_seed_range_behave_as_single_seed(seeds.part2_iter()[0], wf))
    # can_we_squeeze_maps(seeds.part2_iter()[0], wf)
    sub_ranges = []
    for i, seed_range in enumerate(part_iter):
        sub_ranges.extend(recursive_cut_seed_range(seed_range, wf))
        # print(f"Loop #{i}: {sub_ranges}")
    min_loc = 9999999999
    for sr in sub_ranges:
        # Here we just need to test the first seed since they are all projected in the same space and are just
        # incremented, so the first seed is also the minimum of the range.
        loc = wf.walk(sr[0])
        if loc < min_loc:
            min_loc = loc

    end = time.time()
    print(f"Found {len(sub_ranges)} sub ranges of seeds")
    print(f"Solution of part #2: {min_loc} (minimum location) in {end - start:.4f} seconds")

    assert 59370572 == min_loc, f"My Solution is 59370572, yours is {min_loc}"


if __name__ == '__main__':
    sample = Path("part1.txt").read_text()
    better_part2(sample)
