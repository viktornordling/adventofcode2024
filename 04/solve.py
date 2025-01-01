file = open("input.txt", "r")

lines = file.readlines()
total = 0

cells = {}
rows = len(lines)
cols = len(lines[0]) - 1

print(f"rows: {rows}")
print(f"cols: {cols}")

for y in range(rows):
    line = lines[y]
    for x in range(cols):
        cur = line[x]
        cells[(x, y)] = cur


def get_cell(x, y):
    if x < 0 or x >= cols or y < 0 or y >= rows:
        return '.'
    return cells[(x, y)]


def print_cells(rows, cols):
    for y in range(rows):
        for x in range(cols):
            cur = cells[(x, y)]
            print(cur + " ", end="")
        print()


def find_above_below(x, y, up_left, up_right, down_left, down_right):
    ul = get_cell(x - 1, y - 1).lower()
    ur = get_cell(x + 1, y - 1).lower()
    dl = get_cell(x - 1, y + 1).lower()
    dr = get_cell(x + 1, y + 1).lower()
    if up_left == ul and up_right == ur and down_left == dl and down_right == dr:
        return 1
    return 0


def find_words(x, y):
    if cells[(x, y)] != "X":
        return 0
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1), (1, 1), (-1, -1), (-1, 1), (1, -1)]

    word = "XMAS"
    words_found = 0
    for dir in dirs:
        index = 1
        cur = (x, y)
        match = True
        while index < 4:
            cur = (cur[0] + dir[0], cur[1] + dir[1])
            cur_char = get_cell(cur[0], cur[1])
            if cur_char != word[index]:
                match = False
                break
            else:
                index += 1
        if match:
            print(f"Found XMAS in position ({x}, {y}), direction {dir}")
            words_found += 1
    return words_found


print_cells(rows, cols)

for y in range(rows):
    line = lines[y]
    for x in range(cols):
        current = get_cell(x, y)
        if current == "X":
            total += find_words(x, y)

print("Part 1: ", total)

total = 0


for y in range(rows):
    line = lines[y]
    for x in range(cols):
        print(cells[(x, y)])
        if cells[(x, y)] == 'A':
            total += find_above_below(x, y, 'm', 'm', 's', 's')
            total += find_above_below(x, y, 's', 's', 'm', 'm')
            total += find_above_below(x, y, 'm', 's', 'm', 's')
            total += find_above_below(x, y, 's', 'm', 's', 'm')

print("Part 2: ", total)