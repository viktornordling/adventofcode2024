import os
import time
os.system('cls' if os.name == 'nt' else 'clear')

data = open('input.txt', 'r').read()
parts = data.split("\n\n")
cell_lines = parts[0].split("\n")
path = parts[1].split("\n")

total = 0

cells = {}
rows = len(cell_lines)
cols = len(cell_lines[0])
org_robot_pos = (0, 0)

for y in range(rows):
    line = cell_lines[y]
    for x in range(cols):
        cur = line[x]
        cells[(x, y)] = cur
        if cur == '@':
            org_robot_pos = (x, y)
            robot_pos = (x, y)


def print_org_cells():
    print("ORG CELLS")
    for y in range(rows):
        for x in range(cols):
            cur = org_cells[(x, y)]
            print(cur + " ", end="")
        print()
    print("END ORG CELLS")


org_cells = cells.copy()
print_org_cells()

total = 0

print(cells)
print(path)

dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]
dir_map = {'<': (-1, 0), '^': (0, -1), '>': (1, 0), 'v': (0, 1)}


def get_cell(x, y):
    if x < 0 or x >= cols or y < 0 or y >= rows:
        return -1
    return cells[(x, y)]


def get_new_cell(x, y):
    if x < 0 or x >= cols * 2 or y < 0 or y >= rows:
        return -1
    return new_map[(x, y)]


def get_org_cell(x, y):
    if x < 0 or x >= cols or y < 0 or y >= rows:
        return -1
    return org_cells[(x, y)]


def print_cells():
    for y in range(rows):
        for x in range(cols):
            cur = cells[(x, y)]
            print(cur + " ", end="")
        print()


def print_new_map():
    for y in range(rows):
        for x in range(cols * 2):
            cur = new_map[(x, y)]
            print(cur + "", end="")
        print()


def walk(cur, step):
    # print("Moving:", step)
    dir = dir_map[step]
    next = (cur[0] + dir[0], cur[1] + dir[1])
    next_val = get_cell(*next)
    if next_val == '#':
        return cur
    elif next_val == 'O':
        # First check if the boxes _can_ be pushed in this dir.
        next_empty = next
        next_empty_val = get_cell(*next_empty)
        while next_empty_val == 'O':
            next_empty = (next_empty[0] + dir[0], next_empty[1] + dir[1])
            next_empty_val = get_cell(*next_empty)
        if next_empty_val == '.':
            # Put a box in the next empty slot, and put the '@' in the next slot and put a '.' in the cur slut.
            cells[next_empty] = 'O'
            cells[next] = '@'
            cells[cur] = '.'
            return next
        else:
            return cur
    else:
        cells[next] = '@'
        cells[cur] = '.'
        return next


# A box can be pushed in the given dir, if:
# - if either of the two spots is a '#', return false
# - the two spots one step along dir are `.`
# - or, if one or both of those spots contain a box (or two boxes), can_push return true for that box or those boxes
def can_push_up_or_down(box_x, box_y, dir):
    next_pos_1 = (box_x + dir[0], box_y + dir[1])
    next_pos_2 = (box_x + 1 + dir[0], box_y + dir[1])
    next_val_1 = get_new_cell(*next_pos_1)
    next_val_2 = get_new_cell(*next_pos_2)
    if next_val_1 == '#' or next_val_2 == '#':
        return False
    elif next_val_1 == '.' and next_val_2 == '.':
        return True
    elif next_val_1 == '[' and next_val_2 == ']':
        # We have a box directly above us.
        return can_push_up_or_down(*next_pos_1, dir)
    elif next_val_1 == ']' and next_val_2 == '[':
        # We have two boxes above us.
        return can_push_up_or_down(next_pos_1[0] - 1, next_pos_1[1], dir) and can_push_up_or_down(next_pos_1[0] + 1, next_pos_1[1], dir)
    elif next_val_1 == ']' and next_val_2 == '.':
        # We have a box top left.
        return can_push_up_or_down(next_pos_1[0] - 1, next_pos_1[1], dir)
    elif next_val_1 == '.' and next_val_2 == '[':
        # We have a box top right.
        return can_push_up_or_down(*next_pos_2, dir)


# Assuming that a box can be pushed, this returns all boxes that will be pushed.
def boxes_in_push_up_or_down(box_x, box_y, dir):
    next_pos_1 = (box_x + dir[0], box_y + dir[1])
    next_pos_2 = (box_x + 1 + dir[0], box_y + dir[1])
    next_val_1 = get_new_cell(*next_pos_1)
    next_val_2 = get_new_cell(*next_pos_2)
    if next_val_1 == '.' and next_val_2 == '.':
        return [(box_x, box_y)]
    elif next_val_1 == '[' and next_val_2 == ']':
        # We have a box directly above us.
        return boxes_in_push_up_or_down(*next_pos_1, dir) + [(box_x, box_y)]
    elif next_val_1 == ']' and next_val_2 == '[':
        # We have two boxes above us.
        return boxes_in_push_up_or_down(next_pos_1[0] - 1, next_pos_1[1], dir) + boxes_in_push_up_or_down(next_pos_1[0] + 1, next_pos_1[1], dir) + [(box_x, box_y)]
    elif next_val_1 == ']' and next_val_2 == '.':
        # We have a box top left.
        return boxes_in_push_up_or_down(next_pos_1[0] - 1, next_pos_1[1], dir) + [(box_x, box_y)]
    elif next_val_1 == '.' and next_val_2 == '[':
        # We have a box top right.
        return boxes_in_push_up_or_down(*next_pos_2, dir) + [(box_x, box_y)]


# This is for a sideways push.
def can_push_sideways(box_x, box_y, dir):
    if dir[0] == 1:
        next_pos_1 = (box_x + 2 * dir[0], box_y + dir[1])
        next_val_1 = get_new_cell(*next_pos_1)
    else:
        next_pos_1 = (box_x + dir[0], box_y + dir[1])
        next_val_1 = get_new_cell(*next_pos_1)
    if next_val_1 == '#':
        return False
    elif next_val_1 == '.':
        return True
    elif next_val_1 == '[':
        # We have a box to the side of us.
        return can_push_sideways(*next_pos_1, dir)
    elif next_val_1 == ']':
        # We have a box to the side of us.
        return can_push_sideways(next_pos_1[0] - 1, next_pos_1[1], dir)


# Assuming that a box can be pushed, this returns all boxes that will be pushed.
def boxes_in_push(box_x, box_y, dir):
    if dir[0] == 1:
        next_pos_1 = (box_x + 2 * dir[0], box_y + dir[1])
        next_val_1 = get_new_cell(*next_pos_1)
    else:
        next_pos_1 = (box_x + dir[0], box_y + dir[1])
        next_val_1 = get_new_cell(*next_pos_1)
    if next_val_1 == '.':
        return [(box_x, box_y)]
    elif next_val_1 == '[':
        return boxes_in_push(*next_pos_1, dir) + [(box_x, box_y)]
    elif next_val_1 == ']':
        return boxes_in_push(next_pos_1[0] - 1, next_pos_1[1], dir) + [(box_x, box_y)]


def move_boxes_in_dir(boxes_to_push, dir):
    # Set the value in the map of each current block's cell to `.`
    for box in boxes_to_push:
        new_map[(box[0], box[1])] = '.'
        new_map[(box[0] + 1, box[1])] = '.'
    # For each box, get its new pos, and set the '[' and ']' in the right spot.
    for box in boxes_to_push:
        new_map[(box[0] + dir[0], box[1] + dir[1])] = '['
        new_map[(box[0] + 1 + dir[0], box[1] + dir[1])] = ']'


def walk_2(cur, step):
    print("Moving:", step)
    dir = dir_map[step]
    next = (cur[0] + dir[0], cur[1] + dir[1])
    next_val = get_new_cell(*next)
    if next_val == '#':
        return cur
    elif next_val == '[':
        if dir[1] != 0:
            if can_push_up_or_down(*next, dir):
                boxes_to_push = boxes_in_push_up_or_down(*next, dir)
                move_boxes_in_dir(boxes_to_push, dir)
                new_map[next] = '@'
                new_map[cur] = '.'
                return next
            return cur
        else:
            if can_push_sideways(*next, dir):
                boxes_to_push = boxes_in_push(*next, dir)
                move_boxes_in_dir(boxes_to_push, dir)
                new_map[next] = '@'
                new_map[cur] = '.'
                return next
            return cur
    elif next_val == ']':
        if dir[1] != 0:
            if can_push_up_or_down(next[0] - 1, next[1], dir):
                boxes_to_push = boxes_in_push_up_or_down(next[0] - 1, next[1], dir)
                move_boxes_in_dir(boxes_to_push, dir)
                new_map[next] = '@'
                new_map[cur] = '.'
                return next
            return cur
        else:
            if can_push_sideways(next[0] - 1, next[1], dir):
                boxes_to_push = boxes_in_push(next[0] - 1, next[1], dir)
                move_boxes_in_dir(boxes_to_push, dir)
                new_map[next] = '@'
                new_map[cur] = '.'
                return next
            return cur
    else:
        new_map[next] = '@'
        new_map[cur] = '.'
        return next


for line in path:
    for step in line:
        robot_pos = walk(robot_pos, step)
        # print_cells()

for y in range(rows):
    for x in range(cols):
        cur = get_cell(x, y)
        if cur == 'O':
            total += y * 100 + x

print("Part 1:", total)

# Transform the map
print_org_cells()
new_map = {}

for y in range(rows):
    for x in range(cols):
        cur = get_org_cell(x, y)
        if cur == '#':
            new_map[(x * 2, y)] = '#'
            new_map[(x * 2 + 1, y)] = '#'
            # print("##", end="")
        if cur == 'O':
            new_map[(x * 2, y)] = '['
            new_map[(x * 2 + 1, y)] = ']'
            # print("[]", end="")
        elif cur == '.':
            new_map[(x * 2, y)] = '.'
            new_map[(x * 2 + 1, y)] = '.'
            # print("..", end="")
        elif cur == '@':
            new_map[(x * 2, y)] = '@'
            new_map[(x * 2 + 1, y)] = '.'
            # print("@.", end="")
        # print(f"(x, y) = {(x, y)}, (x * 2 + 1, y) = {(x * 2 + 1, y)}")
    print()

print_new_map()

robot_pos = (org_robot_pos[0] * 2, org_robot_pos[1])

step_count = 0

for line in path:
    for step in line:
        if step_count == 2609:
            print_new_map()
        robot_pos = walk_2(robot_pos, step)
        step_count += 1
        os.system('cls' if os.name == 'nt' else 'clear')
        print_new_map()
        for y in range(rows):
            for x in range(cols * 2):
                cur = get_new_cell(x, y)
                left = get_new_cell(x - 1, y)
                if cur == ']' and not left == '[':
                    print(f"fucked after {step_count} steps")
                    print("Fuuuuuuuck")

        time.sleep(0.01)

print_new_map()

total2 = 0
for y in range(rows):
    for x in range(cols * 2):
        cur = get_new_cell(x, y)
        if cur == '[':
            total2 += y * 100 + x

print("Part 2:", total2)
