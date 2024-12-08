from math import prod
import re
import math
import string

file = open("input.txt", "r")

lines = file.readlines()
total = 0

cells = {}
rows = len(lines)
cols = len(lines[0]) - 1

print(f"rows: {rows}")
print(f"cols: {cols}")

guard_pos = (0, 0)

for y in range(rows):
    line = lines[y]
    for x in range(cols):
        cur = line[x]
        cells[(x, y)] = cur
        if cur == '^':
            guard_pos = (x, y)

dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
cur_dir = (-1, 0)


def get_cell(x, y):
    if x < 0 or x >= cols or y < 0 or y >= rows:
        return '-'
    return cells[(x, y)]


def guard_in_grid(guard_pos):
    return get_cell(guard_pos[0], guard_pos[1]) != '-'


while guard_in_grid(guard_pos):
    next_pos = guard_pos[0] + cur_dir[0], guard_pos[1] + cur_dir[1]
    get_cell()