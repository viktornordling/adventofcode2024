file = open("input.txt", "r")

lines = file.readlines()

total = 0
cells = {}
anticells = {}
rows = len(lines)
cols = len(lines[0]) - 1

symbols = set()
symbol_to_pos = {}

for y in range(rows):
    line = lines[y]
    for x in range(cols):
        cur = line[x]
        cells[(x, y)] = cur
        if cur != '.':
            symbols.add(cur)
            positions = []
            if cur in symbol_to_pos:
                positions = symbol_to_pos[cur]
            positions.append((x, y))
            symbol_to_pos[cur] = positions


def reflect_antinodes(pos1, pos2):
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]

    new_pos1 = (pos1[0] - dx, pos1[1] - dy)
    new_pos2 = (pos2[0] + dx, pos2[1] + dy)

    return new_pos1, new_pos2


def reflect_antinodes_2(pos1, pos2, antinode_dict):
    antinode_dict[pos1] = '#'
    antinode_dict[pos2] = '#'
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]

    new_pos1 = (pos1[0] - dx, pos1[1] - dy)
    while in_grid(new_pos1):
        antinode_dict[new_pos1] = '#'
        new_pos1 = (new_pos1[0] - dx, new_pos1[1] - dy)

    new_pos2 = (pos2[0] + dx, pos2[1] + dy)
    while in_grid(new_pos2):
        antinode_dict[new_pos2] = '#'
        new_pos2 = (new_pos2[0] + dx, new_pos2[1] + dy)


def print_cells():
    for y in range(rows):
        for x in range(cols):
            cur = cells[(x, y)]
            print(cur, end="")
        print()


def in_grid(pos):
    return 0 <= pos[0] < rows and 0 <= pos[1] < cols


for symbol, positions in symbol_to_pos.items():
    for i in range(0, len(positions)):
        for j in range(i + 1, len(positions)):
            # Given a pair of symbols, find the two antinodes.
            # First, find the distance between the two antinodes.
            (antinode1, antinode2) = reflect_antinodes(positions[i], positions[j])
            if in_grid(antinode1):
                anticells[antinode1] = '#'
            if in_grid(antinode2):
                anticells[antinode2] = '#'


print_cells()

print("Part 1:", len(anticells))

antinodes2 = {}

for symbol, positions in symbol_to_pos.items():
    for i in range(0, len(positions)):
        for j in range(i + 1, len(positions)):
            # Given a pair of symbols, find the two antinodes.
            # First, find the distance between the two antinodes.
            reflect_antinodes_2(positions[i], positions[j], antinodes2)


print("Part 2:", len(antinodes2))

