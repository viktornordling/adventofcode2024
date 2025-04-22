import heapq

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
            start = (x, y)
        elif cur == 'E':
            goal = (x, y)


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


def reconstruct_path(came_from, start, goal):
    path = []
    current_pos = goal
    while current_pos != start:
        path.append(current_pos)
        current_pos = came_from[current_pos]
    path.append(start)
    path.reverse()

    return path


def get_cell(x, y):
    if x < 0 or x >= cols or y < 0 or y >= rows:
        return '#'
    thingo = cells.get((x, y), '.')
    return thingo


def get_neighbors(current, grid):
    neighbors = []
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for direction in directions:
        npos = (current[0] + direction[0], current[1] + direction[1])
        cell = get_cell(npos[0], npos[1])
        if cell != '#':
            neighbors.append(npos)
    return neighbors


def cost(_current, _neighbor):
    return 1


def heuristic(node, goal):
    manhattan_dist = abs(node[0] - goal[0]) + abs(node[1] - goal[1])
    return manhattan_dist


def a_star(start, goal, grid):
    open_set = PriorityQueue()
    open_set.put(start, 0)

    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not open_set.empty():
        current = open_set.get()

        if (current[0], current[1]) == goal:
            return reconstruct_path(came_from, start, current)

        for neighbor in get_neighbors(current, grid):
            new_cost = cost_so_far[current] + cost(current, neighbor)
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic(neighbor, goal)
                open_set.put(neighbor, priority)
                came_from[neighbor] = current

    return None


cell_to_dist = {}
cells_on_path = []


def get_length_of_shortest_path(start, goal, grid):
    path = a_star(start, goal, grid)
    steps = 0
    for cell in path:
        cell_to_dist[cell] = steps
        steps += 1
        cells_on_path.append(cell)
    return len(path) - 1


print(f"Finding path from {start} to {goal}")
shortest = get_length_of_shortest_path(start, goal, cells)
print(f"Shortest path is of length: {shortest}")


def get_adjacents(x, y):
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1), (1, 1), (-1, -1), (-1, 1), (1, -1)]
    cells = [get_cell(x + dir[0], y + dir[1]) for dir in dirs]
    return cells


orig = shortest
cheats = 0

def print_cells():
    for y in range(rows):
        for x in range(cols):
            cur = cells[(x, y)]
            print(cur, end="")
        print()


print_cells()

# for y in range(rows):
#     for x in range(cols):
#         # if a cell is a wall, and it has at least 2 non wall cells around it, it would make sense to try removing it
#         # as a cheat.
#         cur = get_cell(x, y)
#         if cur == '#':
#             open_count = 0
#             for neighbor in get_adjacents(x, y):
#                 if neighbor == '.':
#                     open_count += 1
#             if open_count >= 2:
#                 # print(f"Testing cheat by removing wall on ({x}, {y})")
#                 cells[(x, y)] = '.'
#                 length = get_length_of_shortest_path(start, goal, cells)
#                 # print(f"Length is then  {length}")
#                 cells[(x, y)] = '#'
#                 saved = orig - length
#                 if saved >= 100:
#                     print(f"Saving {saved} cells")
#                     cheats += 1

path_length = len(cells_on_path)
cheat_length = 2
for i in range(path_length):
    # print(f"i = {i} of {path_length}")
    for j in range(i + 1, path_length):
        cell_i = cells_on_path[i]
        cell_j = cells_on_path[j]
        # print(f"Checking for cheats between cell {cell_i} and cell {cell_j}")
        manhattan_dist = abs(cell_i[0] - cell_j[0]) + abs(cell_i[1] - cell_j[1])
        if manhattan_dist <= cheat_length:
            dist_with_cheat = cell_to_dist[cell_i] + (orig - cell_to_dist[cell_j]) + manhattan_dist
            saved = orig - dist_with_cheat
            if saved >= 100:
                # print(f"Saving {saved} cells")
                cheats += 1

print("Part 1:", cheats)

cheats = 0

cheat_length = 20
for i in range(path_length):
    # print(f"i = {i} of {path_length}")
    for j in range(i + 1, path_length):
        cell_i = cells_on_path[i]
        cell_j = cells_on_path[j]
        # print(f"Checking for cheats between cell {cell_i} and cell {cell_j}")
        manhattan_dist = abs(cell_i[0] - cell_j[0]) + abs(cell_i[1] - cell_j[1])
        if manhattan_dist <= cheat_length:
            dist_with_cheat = cell_to_dist[cell_i] + (orig - cell_to_dist[cell_j]) + manhattan_dist
            saved = orig - dist_with_cheat
            if saved >= 100:
                # print(f"Saving {saved} cells")
                cheats += 1

print("Part 2:", cheats)