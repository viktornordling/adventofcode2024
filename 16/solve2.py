import heapq
import math

file = open("input.txt", "r")
lines = file.readlines()

total_2 = 0
cells = {}
rows = len(lines)
cols = len(lines[0]) - 1

start = None
goal = None

for y in range(rows):
    line = lines[y]
    for x in range(cols):
        cur = line[x]
        cells[(x, y)] = cur
        if cur == 'S':
            start = (x, y, 'E')
        elif cur == 'E':
            goal = (x, y, 'N')


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


def dijkstra(start, goal, grid):
    open_set = PriorityQueue()
    open_set.put(start, 0)

    prev = {start: []}
    cost_so_far = {start: 0}

    while not open_set.empty():
        current = open_set.get()
        # print(f"current: {current}")

        if current == goal:
            continue

        for neighbor in get_neighbors(current, grid):
            new_cost = cost_so_far[current] + cost(current, neighbor)
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                open_set.put(neighbor, new_cost)
                prev[neighbor] = [current]
                if neighbor[0] == 5 and neighbor[1] == 7:
                    print(f"neighbor {neighbor}, cost: {new_cost}, prev = {prev[neighbor]}")
            elif new_cost == cost_so_far[neighbor]:
                prev[neighbor].append(current)

    good_cells = set()
    for key, value in prev.items():
        for cell in value:
            cell_pos = (cell[0], cell[1])
            good_cells.add(cell_pos)

    print("Good cells: ",len(good_cells))
    print_cells()
    total = 0
    for key, val in cells.items():
        if val == 'O':
            total += 1

    print("Total:", total)
    return prev, cost_so_far


def get_neighbors(current, grid):
    neighbors = []
    neighbor = move(current)
    if is_valid(neighbor, grid):
        neighbors.append(neighbor)
    turns = get_turns(current[2])
    for turn in turns:
        turned_pos = (current[0], current[1], turn)
        neighbors.append(turned_pos)
    return neighbors


def cost(current, neighbor):
    if current[2] == neighbor[2]:
        return 1
    else:
        return 1000


def print_cells():
    for y in range(rows):
        for x in range(cols):
            cur = cells.get((x, y), '.')
            print(cur, end="")
        print()


def is_valid(node, grid):
    pos = (node[0], node[1])
    return pos in grid and not grid[pos] == '#'


def move(current):
    x, y, facing = current
    if facing == 'N':
        return x, y - 1, facing
    elif facing == 'E':
        return x + 1, y, facing
    elif facing == 'S':
        return x, y + 1, facing
    elif facing == 'W':
        return x - 1, y, facing


def get_turns(facing):
    if facing == 'N':
        return ['E', 'W']
    elif facing == 'E':
        return ['N', 'S']
    elif facing == 'S':
        return ['E', 'W']
    elif facing == 'W':
        return ['N', 'S']


def dfs_paths(prev, start, goal):
    stack = [(goal, [goal])]
    all_nodes = set()
    while stack:
        (vertex, path) = stack.pop()
        if vertex[0] == 5 and vertex[1] == 7:
            print("stop it!")
        if vertex == start:
            all_nodes.update(path)

        for next in prev.get(vertex, []):
            if next not in path:
                stack.append((next, path + [next]))
    return all_nodes


prev, cost_so_far = dijkstra(start, goal, cells)

dirs = [(goal[0], goal[1], 'N'), (goal[0], goal[1], 'E'), (goal[0], goal[1], 'S'), (goal[0], goal[1], 'W')]
a = cost_so_far.get(dirs[0], math.inf)
b = cost_so_far.get(dirs[1], math.inf)
c = cost_so_far.get(dirs[2], math.inf)
d = cost_so_far.get(dirs[3], math.inf)

min_cost = min(a, b, c, d)

for dir in dirs:
    if cost_so_far.get(dir, math.inf) == min_cost:
        print(f"best dir: {dir}")
        all_nodes_in_paths = dfs_paths(prev, start, dir)
        uniq = set()
        for n in all_nodes_in_paths:
            cells[(n[0], n[1])] = 'O'
            uniq.add((n[0], n[1]))
        print_cells()
        print("Num nodes in all shortest paths:", len(uniq))
