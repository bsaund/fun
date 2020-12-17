from utils import iteration
import numpy as np

state_str = """..#..#.#
##.#..#.
#....#..
.#..####
.....#..
...##...
.#.##..#
.#.#.#.#"""
# state_str = """.#.
# ..#
# ###"""

state = [[[int(l == "#")] for l in line] for line in state_str.split("\n")]


def count_neighbors(s, x, y, z):
    subselected = iteration.subselect_3d(s, x, y, z, 1, 1, 1, exclude_center=True)
    return sum([sum([sum(line) for line in slice]) for slice in subselected])


def print_state(s):
    for i in range(np.array(s).shape[2]):
        print(f"layer = {i}")
        print(np.array(s)[:, :, i])

    print('----------------------------')


def update_state(s):
    def new_value(x, y, z):
        neighbors = count_neighbors(s, x, y, z)
        is_occupied = 0 <= x < len(s) and 0 <= y < len(s[0]) and 0 <= z < len(s[0][0]) and s[x][y][z]
        if is_occupied:
            return int(neighbors == 2 or neighbors == 3)
        return int(neighbors == 3)

    return [[[new_value(x - 1, y - 1, z - 1) for z in range(len(s[0][0]) + 2)] for y in range(len(s[0]) + 2)] for x in
            range(len(s) + 2)]


s = state
# print_state(s)
for i in range(6):
    s = update_state(s)
    # print_state(s)

print(sum([sum([sum(line) for line in slice]) for slice in s]))

# Part 2
# It too me way too long to realize this is more complicated than necessary, and grows impractically large too quickly
# s = [state]
#
#
# def count_neighbors4(arr, x, y, z, w):
#     subselected = iteration.subselect_4d(arr, (x, y, z, w), (1, 1, 1, 1), exclude_center=True)
#     return np.sum(np.array(subselected))
#
#
# def update_state4(s):
#     def new_value(x, y, z, w):
#         neighbors = count_neighbors4(s, x, y, z, w)
#         is_occupied = 0 <= x < len(s) and 0 <= y < len(s[0]) and \
#                       0 <= z < len(s[0][0]) and 0 <= w < len(s[0][0][0]) \
#                       and s[x][y][z][w]
#         if is_occupied:
#             return int(neighbors == 2 or neighbors == 3)
#         return int(neighbors == 3)
#
#     return [
#         [[[new_value(x - 1, y - 1, z - 1, w - 1) for w in range(len(s[0][0][0]) + 2)] for z in range(len(s[0][0]) + 2)]
#          for y in range(len(s[0]) + 2)] for x in
#         range(len(s) + 2)]
#
#
# def trim_state(s):
#     s = np.array(s)
#     if np.sum(s[0, :, :, :]) == 0:
#         s = s[1:, :, :, :]
#     if np.sum(s[:, 0, :, :]) == 0:
#         s = s[:, 1:, :, :]
#     if np.sum(s[:, :, 0, :]) == 0:
#         s = s[:, :, 1:, :]
#     if np.sum(s[:, :, :, 0]) == 0:
#         s = s[:, :, :, 1:]
#     if np.sum(s[-1, :, :, :]) == 0:
#         s = s[:-2, :, :, :]
#     if np.sum(s[:, -1, :, :]) == 0:
#         s = s[:, :-2, :, :]
#     if np.sum(s[:, :, :, -1]) == 0:
#         s = s[:, :, :-2, :]
#     if np.sum(s[:, :, :, -1]) == 0:
#         s = s[:, :, :, :-2]
#     return s.tolist()
#
#     # s = update_state4(s)
#
#
# for i in range(6):
#     print(f'size at {i}: {np.array(s).size}')
#     s = update_state4(s)
#     s = trim_state(s)
#
# print(np.sum(np.array(s)))

from collections import defaultdict

state = [(i, j, 0, 0) for j, line in enumerate(state_str.split('\n')) for i, val in enumerate(line) if val == "#"]

dirs = [(a, b, c, d) for a in range(-1, 2) for b in range(-1, 2) for c in range(-1, 2) for d in range(-1, 2) if
        not (a == 0 and b == 0 and c == 0 and d == 0)]


def update_4d(s):
    counts = defaultdict(lambda: 0)
    for occ_coord in s:
        for d in dirs:
            counts[tuple(a + b for a,b in zip(occ_coord, d))] += 1

    new_state = []
    for coord, count in counts.items():
        if count == 3:
            new_state.append(coord)
        if count == 2 and coord in s:
            new_state.append(coord)
    return new_state


for i in range(6):
    print(len(state))
    state = update_4d(state)

print(len(state))
