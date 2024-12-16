file = open("input.txt", "r")

lines = file.readlines()

cells = {}
rows = len(lines)
cols = len(lines[0]) - 1

heads = []

for y in range(rows):
    line = lines[y]
    for x in range(cols):
        cur = line[x]
        num = int(cur)
        cells[(x, y)] = num
        if num == 0:
            heads.append((x, y))

total = 0


def get_cell(x, y):
    if x < 0 or x >= cols or y < 0 or y >= rows:
        return -1
    return cells[(x, y)]


dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]
peaks = []
visited = set()


def dfs(cur):
    cur_cell = get_cell(*cur)
    visited.add(cur)
    if cur_cell == 9:
        peaks.append(cur)
    else:
        for dir in dirs:
            neighbor = (cur[0] + dir[0], cur[1] + dir[1])
            neighbor_value = get_cell(*neighbor)
            if neighbor_value == cur_cell + 1 and neighbor not in visited:
                dfs(neighbor)


for head in heads:
    peaks = []
    visited = set()
    dfs(head)
    total += len(peaks)

print("Part 1:", total)

total = 0


def dfs_2(cur, rec_visited):
    cur_cell = get_cell(*cur)
    # visited.add(cur)
    if cur_cell == 9:
        peaks.append(cur)
    else:
        for dir in dirs:
            neighbor = (cur[0] + dir[0], cur[1] + dir[1])
            neighbor_value = get_cell(*neighbor)
            if neighbor_value == cur_cell + 1 and neighbor not in rec_visited:
                rec_visited.add(neighbor)
                dfs_2(neighbor, rec_visited)
                rec_visited.remove(neighbor)


for head in heads:
    peaks = []
    visited = set()
    dfs_2(head, set())
    total += len(peaks)

print("Part 2:", total)
