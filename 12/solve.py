file = open("input.txt", "r")

lines = file.readlines()

total_2 = 0

cells = {}
rows = len(lines)
cols = len(lines[0]) - 1

for y in range(rows):
    line = lines[y]
    for x in range(cols):
        cur = line[x]
        cells[(x, y)] = cur


visited = set()
regions = {}

dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def get_cell(x, y):
    if x < 0 or x >= cols or y < 0 or y >= rows:
        return -1
    return cells[(x, y)]


def dfs(start, cur_cell):
    visited.add(cur_cell)
    start_val = get_cell(*start)
    key = start
    # print(f"key = {key} start_val = {start_val}")
    region = regions.get(key, set())
    region.add(cur_cell)
    regions[key] = region
    for dir in dirs:
        next = cur_cell[0] + dir[0], cur_cell[1] + dir[1]
        next_val = get_cell(*next)
        if next not in visited and next_val != -1 and next_val == start_val:
            dfs(start, next)


for i in range(rows):
    for j in range(cols):
        if (i, j) not in visited:
            dfs((i, j), (i, j))


def get_circumference(region):
    circumference = 0
    for cell in region:
        for dir in dirs:
            next = cell[0] + dir[0], cell[1] + dir[1]
            if next not in region:
                circumference += 1
    return circumference


def get_circumference_2(region):
    circumference = {}
    dir_names = ["up", "right", "down", "left"]
    for cell in region:
        for index, dir in enumerate(dirs):
            next = cell[0] + dir[0], cell[1] + dir[1]
            if next not in region:
                circumference[(cell[0], cell[1], dir_names[index])] = 'X'
    return circumference


def fence_has_left(pos, side, circ: dict):
    left = (pos[0] - 1, pos[1], side)
    return left in circ


def get_left(pos, side, circ: dict):
    left = (pos[0] - 1, pos[1], side)
    if left not in circ:
        return None
    return left


def fence_has_up(pos, side, circ: dict):
    left = (pos[0], pos[1] - 1, side)
    return left in circ


def get_up(pos, side, circ):
    up = (pos[0], pos[1] - 1, side)
    if up not in circ:
        return None
    return up


def get_down(pos, side, circ: dict):
    down = pos[0], pos[1] + 1, side
    if down not in circ:
        return None
    return down


def get_right(pos, side, circ: dict):
    right = pos[0] + 1, pos[1], side
    if right not in circ:
        return None
    return right


def count_lines(circ: dict):
    min_x = min([fence[0] for fence in circ])
    max_x = max([fence[0] for fence in circ])

    min_y = min([fence[1] for fence in circ])
    max_y = max([fence[1] for fence in circ])

    lines = 0
    for cur_x in range(min_x, max_x + 1):
        # Trace along "left".
        last = None
        for cur_y in range(min_y, max_y + 1):
            if (cur_x, cur_y, 'left') in circ:
                if last == None:
                    last = (cur_x, cur_y)
                    lines += 1
                elif last != None:
                    last = (cur_x, cur_y)
            else:
                last = None
        # Trace along "right".
        last = None
        for cur_y in range(min_y, max_y + 1):
            if (cur_x, cur_y, 'right') in circ:
                if last == None:
                    last = (cur_x, cur_y)
                    lines += 1
                elif last != None:
                    last = (cur_x, cur_y)
            else:
                last = None


    for cur_y in range(min_y, max_y + 1):
        # Trace along "down"
        last = None
        for cur_x in range(min_x, max_x + 1):
            if (cur_x, cur_y, 'down') in circ:
                if last == None:
                    last = (cur_x, cur_y)
                    lines += 1
                elif last != None:
                    last = (cur_x, cur_y)
            else:
                last = None
        # Trace along "up"
        last = None
        for cur_x in range(min_x, max_x + 1):
            if (cur_x, cur_y, 'up') in circ:
                if last == None:
                    last = (cur_x, cur_y)
                    lines += 1
                elif last != None:
                    last = (cur_x, cur_y)
            else:
                last = None
    return lines


total_1 = 0
total_2 = 0
for region_key, region in regions.items():
    circumference = get_circumference(region)
    circumference_cells = get_circumference_2(region)
    lines = count_lines(circumference_cells)

    cost_1 = circumference * len(region)
    total_1 += cost_1

    cost_2 = lines * len(region)
    total_2 += cost_2


print("Part 1:", total_1)
print("Part 2:", total_2)

