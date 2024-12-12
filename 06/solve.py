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


dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]
cur_dir = (0, -1)
cur_dir_index = 0
original_guard_pos = guard_pos


def get_cell(cell):
    x, y = cell
    if x < 0 or x >= cols or y < 0 or y >= rows:
        return '-'
    return cells[(x, y)]


def guard_in_grid(guard_pos):
    return get_cell(guard_pos) != '-'


visited_cells = set()
visited_cells.add(guard_pos)

while guard_in_grid(guard_pos):
    next_pos = guard_pos[0] + cur_dir[0], guard_pos[1] + cur_dir[1]
    if get_cell(next_pos) == '#':
        cur_dir_index += 1
        if cur_dir_index >= len(dirs):
            cur_dir_index = 0
        cur_dir = dirs[cur_dir_index]
    else:
        if get_cell(next_pos) != '-':
            visited_cells.add(next_pos)
            cells[next_pos] = 'X'
        guard_pos = next_pos

visited = 0

for pos, val in cells.items():
    print(f"pox = {pos}, val = {val}")
    if val == 'X':
        visited += 1


def print_cells():
    for y in range(rows):
        for x in range(cols):
            cur = cells[(x, y)]
            print(cur, end="")
        print()


print_cells()

print("Part 1:", len(visited_cells))

total = 0


def guard_gets_stuck():
    guard_pos = original_guard_pos
    cur_dir = (0, -1)
    cur_dir_index = 0

    visited_cells_with_dirs = set()

    # print("Checking if guard gets stuck given the grid looks like this:")
    # print_cells()

    while guard_in_grid(guard_pos):
        if (guard_pos, cur_dir_index) in visited_cells_with_dirs:
            return True
        visited_cells_with_dirs.add((guard_pos, cur_dir_index))
        next_pos = guard_pos[0] + cur_dir[0], guard_pos[1] + cur_dir[1]
        if get_cell(next_pos) == '#':
            cur_dir_index += 1
            if cur_dir_index >= len(dirs):
                cur_dir_index = 0
            cur_dir = dirs[cur_dir_index]
        else:
            if get_cell(next_pos) != '-':
                cells[next_pos] = 'X'
            guard_pos = next_pos
    return False


for cell in visited_cells:
    if cell == original_guard_pos:
        continue
    cells[cell] = '#'
    if guard_gets_stuck():
        total += 1
    cells[cell] = 'X'

print("Part 2:", total)
