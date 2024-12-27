import functools
from collections import deque
from functools import cmp_to_key

file = open("input.txt", "r")

lines = file.readlines()

total = 0

button_graph = {}
button_graph[7] = [(4, 'v'), (8, '>')]
button_graph[8] = [(7, '<'), (9, '>'), (5, 'v')]
button_graph[9] = [(8, '<'), (6, 'v')]

button_graph[4] = [(7, '^'), (1, 'v'), (5, '>')]
button_graph[5] = [(8, '^'), (4, '<'), (2, 'v'), (6, '>')]
button_graph[6] = [(5, '<'), (9, '^'), (3, 'v')]

button_graph[1] = [(4, '^'), (2, '>')]
button_graph[2] = [(1, '<'), (5, '^'), (3, '>'), (0, 'v')]
button_graph[3] = [(6, '^'), ('A', 'v'), (2, '<')]

button_graph[0] = [('A', '>'), (2, '^')]
button_graph['A'] = [(0, '<'), (3, '^')]

# Arrow button graph

arrow_button_graph = {}
arrow_button_graph['^'] = [('v', 'v'), ('A', '>')]
arrow_button_graph['A'] = [('^', '<'), ('>', 'v')]
arrow_button_graph['<'] = [('v', '>')]
arrow_button_graph['v'] = [('^', '^'), ('<', '<'), ('>', '>')]
arrow_button_graph['>'] = [('v', '<'), ('A', '^')]


def compare_numpad(item1, item2):
    # print(f"Comparing {item1} and {item2}")
    # Make < come before ^, because ^ is closer to A, so we want that last.
    if item1 == '<' and item2 == '^':
        return -1
    elif item1 == '^' and item2 == '<':
        return 1
    # > and ^ are at the same diff from A, so it doesn't really matter.
    # If we do > before ^, we don't risk moving up into the empty spot.
    elif item1 == '>' and item2 == '^':
        return -1
    # Same but other way around.
    elif item1 == '^' and item2 == '>':
        return 1
    # Make < come before v, because v is closer to A, so we want that last.
    elif item1 == '<' and item2 == 'v':
        return -1
    # Same but other way around.
    elif item1 == 'v' and item2 == '<':
        return 1
    # Make v come before >, because > is closer to A, so we want that last.
    elif item1 == 'v' and item2 == '>':
        return -1
    # Same but other way around.
    elif item1 == '>' and item2 == 'v':
        return 1
    else:
        if item1 < item2:
            return -1
        else:
            return 1


def compare_arrow_pad(item1, item2):
    if item1 == item2:
        return 0
    # Make < come before ^, because ^ is closer to A, so we want that last.
    if item1 == '<' and item2 == '^':
        return -1
    elif item1 == '^' and item2 == '<':
        return 1
    # > and ^ are at the same diff from A, so it doesn't really matter.
    # If we do > before ^, we don't risk moving up into the empty spot.
    elif item1 == '>' and item2 == '^':
        return -1
    # Same but other way around.
    elif item1 == '^' and item2 == '>':
        return 1
    # Make < come before v, because v is closer to A, so we want that last.
    elif item1 == '<' and item2 == 'v':
        return -1
    # Same but other way around.
    elif item1 == 'v' and item2 == '<':
        return 1
    # Make v come before >, because > is closer to A, so we want that last.
    elif item1 == 'v' and item2 == '>':
        return -1
    # Same but other way around.
    elif item1 == '>' and item2 == 'v':
        return 1
    else:
        if item1 < item2:
            return -1
        else:
            return 1


def use_manual_num_path(start, target):
    return (start in [0, 'A'] and target in [1, 4, 7]) or (target in [0, 'A'] and start in [1, 4, 7])


def get_manual_num_path(start, target):
    if start == 0:
        if target == 1:
            return ['^', '<']
        elif target == 4:
            return ['^', '^', '<']
        elif target == 7:
            return ['^', '^', '^', '<']
    if start == 'A':
        if target == 1:
            return ['^', '<', '<']
        elif target == 4:
            return ['^', '^', '<', '<']
        elif target == 7:
            return ['^', '^', '^', '<', '<']
    if start == 1:
        if target == 0:
            return ['>', 'v']
        if target == 'A':
            return ['>', 'v', '>']
    if start == 4:
        if target == 0:
            return ['>', 'v', 'v']
        if target == 'A':
            return ['>', 'v', 'v', '>']
    if start == 7:
        if target == 0:
            return ['>', 'v', 'v', 'v']
        if target == 'A':
            return ['>', '>', 'v', 'v', 'v']


def use_manual_arrow_path(start, target):
    return (start in ['^', 'A'] and target in ['<']) or (start in ['<'] and target in ['^', 'A'])


def get_manual_arrow_path(start, target):
    if start == 'A':
        return ['v', '<', '<']
    if start == '^':
        return ['v', '<']
    if start == '<':
        if target == 'A':
            return ['>', '>', '^']
        elif target == '^':
            return ['>', '^']


def bfs(start, target, graph, comparator):
    queue = deque([(start, [])])
    visited = set([start])

    while queue:
        current, path = queue.popleft()
        if current == target:
            # print("Sorting path:", path)
            sorted_path = sorted(path, key=cmp_to_key(comparator))
            # print("Sorted path:", sorted_path)
            return sorted_path

        for (neighbor, direction) in graph.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [direction]))
    return None


@functools.cache
def find_shortest_num_path(current, num):
    return bfs(current, num, button_graph, compare_numpad)


@functools.cache
def find_shortest_arrow_path(current, num):
    return bfs(current, num, arrow_button_graph, compare_arrow_pad)


def press_num_buttons(sequence):
    current = 'A'
    presses = []
    for num in sequence.strip():
        if num != 'A':
            num = int(num)
        if use_manual_num_path(current, num):
            presses.extend(get_manual_num_path(current, num))
        else:
            presses.extend(find_shortest_num_path(current, num))
        current = num
        presses.append('A')
    return presses


def press_arrow_buttons(sequence):
    current = 'A'
    presses = []
    for button in sequence.strip():
        if use_manual_arrow_path(current, button):
            presses.extend(get_manual_arrow_path(current, button))
        else:
            presses.extend(find_shortest_arrow_path(current, button))
        current = button
        presses.append('A')
    return presses


def follow_arrow_instructions(sequence):
    current = 'A'
    result = []
    for button in sequence.strip():
        if button == 'A':
            result.append(current)
        transitions = arrow_button_graph.get(current)
        for transition in transitions:
            if transition[1] == button:
                current = transition[0]
                break
    return result


def follow_num_instructions(sequence):
    current = 'A'
    result = []
    for button in sequence.strip():
        if button == 'A':
            result.append(current)
        transitions = button_graph.get(current)
        for transition in transitions:
            if transition[1] == button:
                current = transition[0]
                break
    return result


def parse_integer(string):
    g = string.lstrip('0').strip()
    return int(g[:-1])


for line in lines:
    print(line)
    presses = press_num_buttons(line)
    num_presses = ''.join(presses)
    print(num_presses)
    first_arrow_presses = press_arrow_buttons(num_presses)
    second_arrow_presses = ''.join(first_arrow_presses)
    print(second_arrow_presses)
    cur = second_arrow_presses
    for i in range(25):
        print(i)
        cur = press_arrow_buttons(''.join(cur))
        # print(''.join(cur))
        print(len(cur))
    total += parse_integer(line) * len(cur)


print("Part 1:", total)
