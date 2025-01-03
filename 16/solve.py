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
            start = (x, y, 'E')
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


def a_star(start, goal, grid):
    open_set = PriorityQueue()
    open_set.put(start, 0)

    came_from = {}
    cost_so_far = {}
    # start_pos = (start[0], start[1])
    came_from[start] = None
    cost_so_far[start] = 0

    while not open_set.empty():
        current = open_set.get()
        print(f"current: {current}")

        if (current[0], current[1]) == goal:
            return reconstruct_path(came_from, start, current)

        for neighbor in get_neighbors(current, grid):
            # current_pos = (current[0], current[1])
            new_cost = cost_so_far[current] + cost(current, neighbor)
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                # neighbor_ = (neighbor[0], neighbor[1])
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic(neighbor, goal, current[2])
                open_set.put(neighbor, priority)
                print(f"Adding {current} as the came_from for {neighbor}")
                came_from[neighbor] = current

    return None  # No path found


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


def heuristic(node, goal, current_direction):
    # Manhattan distance
    manhattan_dist = abs(node[0] - goal[0]) + abs(node[1] - goal[1])

    # Determine the direction to the goal
    goal_direction = determine_direction(node, goal)

    # Calculate the number of turns needed
    turns_needed = calculate_turns(current_direction, goal_direction)

    return manhattan_dist + turns_needed * 1000


def print_cells():
    # os.system('cls' if os.name == 'nt' else 'clear')
    for y in range(rows):
        for x in range(cols):
            cur = cells.get((x, y), '.')
            print(cur, end="")
        print()


def determine_direction(node, goal):
    dx = goal[0] - node[0]
    dy = goal[1] - node[1]
    if abs(dx) > abs(dy):
        return 'E' if dx > 0 else 'W'
    else:
        return 'S' if dy > 0 else 'N'


def calculate_turns(current_direction, goal_direction):
    directions = ['N', 'E', 'S', 'W']
    current_index = directions.index(current_direction)
    goal_index = directions.index(goal_direction)
    return min(abs(goal_index - current_index), 4 - abs(goal_index - current_index))


def reconstruct_path(came_from, start, goal):
    path = []
    current_pos = goal
    while current_pos != start:
        path.append(current_pos)
        current_pos = came_from[current_pos]
        # current_pos = (current[0], current[1])
    path.append(start)
    path.reverse()

    cur_pos = path[0]
    cur_pos = (cur_pos[0], cur_pos[1])
    cost = 0
    for step in path[1:]:
        step_pos = (step[0], step[1])
        if step_pos == cur_pos:
            # we're just turning, add 1000
            print(f"step = {step}, we're turning")
            cost += 1000
        else:
            cost += 1
        cur_pos = (step[0], step[1])
        cells[(step_pos[0], step_pos[1])] = 'x'

    print(f"Path cost: {cost}")
    print_cells()

    return path


def is_valid(node, grid):
    pos = (node[0], node[1])
    return pos in grid and not grid[pos] == '#'


def is_valid_turn(turn, grid):
    return is_valid(turn, grid)


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


def turn_direction(current_direction, turn):
    directions = ['N', 'E', 'S', 'W']
    current_index = directions.index(current_direction)

    if turn == 'left':
        new_index = (current_index - 1) % 4
    elif turn == 'right':
        new_index = (current_index + 1) % 4
    else:
        raise ValueError("Invalid turn direction")

    return directions[new_index]


# Example usage:
path = a_star(start, goal, cells)

print("Path:", path)
