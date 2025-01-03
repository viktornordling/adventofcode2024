import heapq

file = open("input.txt", "r")

lines = file.readlines()

total_2 = 0

cells = {}

rows = 71
cols = 71
bytes_to_simulate = 1024

start = None
goal = None
bytes = []


for line in lines:
    x, y = map(int, line.split(","))
    bytes.append((x, y))

for i in range(bytes_to_simulate):
    byte = bytes[i]
    cells[byte] = '#'


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


def print_cells():
    for y in range(rows):
        for x in range(cols):
            cur = get_cell(x, y)
            print(cur, end="")
        print()


def reconstruct_path(came_from, start, goal):
    path = []
    current_pos = goal
    while current_pos != start:
        path.append(current_pos)
        current_pos = came_from[current_pos]
    path.append(start)
    path.reverse()

    cost = 0
    for step in path[1:]:
        step_pos = (step[0], step[1])
        cost += 1
        cells[(step_pos[0], step_pos[1])] = 'O'

    return path, cost


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


path, path_cost = a_star((70, 70), (0, 0), cells)
print("Part 1:", path_cost)

for i in range(1024, len(bytes)):
    byte = bytes[i]
    cells[byte] = '#'
    path = a_star((70, 70), (0, 0), cells)
    if path is None:
        print("Part 2:", byte)
