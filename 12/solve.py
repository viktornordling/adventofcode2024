file = open("input.txt", "r")

lines = file.readlines()

total = 0

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
    circ = 0
    for cell in region:
        for dir in dirs:
            next = cell[0] + dir[0], cell[1] + dir[1]
            # neigh = get_cell(*next)
            if next not in region:
                circ += 1
    return circ


# def get_sides(circ):
#     first = circ.to_list()[0]
#
#     def dfs_sides(cur):



# print(regions)
# print(len(regions))
total = 0
for region_key, region in regions.items():
    circ = get_circumference(region)
    cost = circ * len(region)
    total += cost
    # print(f"{region_key}: {circ}, cost: {cost}")


# print(regions)
print("Part 1:", total)

