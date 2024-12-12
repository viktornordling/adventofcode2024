from collections import deque
from functools import cmp_to_key

lines = open('input.txt', 'r').read()
parts = lines.split("\n\n")
rules = parts[0].split("\n")
prints = parts[1].split("\n")

page_to_afters = {}
page_to_befores = {}

all_pages = set()

for rule in rules:
    left, right = [int(x) for x in rule.split("|")]
    all_pages.add(left)
    all_pages.add(right)

for page in all_pages:
    page_to_afters[page] = set()
    page_to_befores[page] = set()

for rule in rules:
    left, right = [int(x) for x in rule.split("|")]
    afters = page_to_afters[left]
    afters.add(right)
    page_to_afters[left] = afters

    befores = page_to_befores[right]
    befores.add(left)
    page_to_befores[right] = befores

# print(f"page_to_afters: {page_to_afters}")
# print(f"page_to_befores: {page_to_befores}")

pages_in_order = list()
first_page = -1

for page, befores in page_to_befores.items():
    if len(befores) == 0:
        # pages_in_order.append(page)
        first_page = page

total = 0
wrongs = []

for line in prints:
    # print(f"Handling line: {line}")
    pages_to_print = [int(x) for x in line.split(",")]
    printed = set()
    good = True
    for num in pages_to_print:
        # print(f"Printing {num}")
        afters = page_to_afters[num]
        for after in afters:
            if after in printed:
                # print(f"{after} should be after {num}, but it has already been printed!")
                good = False
                break
        if not good:
            break
        printed.add(num)
    if good:
        middle = pages_to_print[len(pages_to_print) // 2]
        total += middle
        # print("Good!")
    else:
        wrongs.append(line)
        # print("Bad!")

print("Part 1:", total)


def before(item1, item2):
    # print(f"Is {item1} before {item2}?")
    checked = set()
    afters = page_to_afters[item1]
    if item2 in afters:
        return True
    queue = deque()
    for after in afters:
        queue.append(after)
    while queue:
        popped = queue.popleft()
        checked.add(popped)
        if popped == item2:
            return True
        if popped not in checked:
            afters = page_to_afters[popped]
            for after in afters:
                if popped not in checked:
                    queue.append(after)
    return False


def compare(item1, item2):
    if before(item1, item2):
        return -1
    elif before(item2, item1):
        return 1
    return 0


def check_order(pages):
    printed = set()
    good = True
    for num in pages:
        afters = page_to_afters[num]
        for after in afters:
            if after in printed:
                good = False
                break
        if not good:
            break
        printed.add(num)
    return good


total = 0
for line in wrongs:
    # print(f"Handling line: {line}")
    pages_to_print = [int(x) for x in line.split(",")]
    fixed = sorted(pages_to_print, key=cmp_to_key(compare))
    print(f"Incorrect sort order: {pages_to_print}, correct:{fixed}")
    # print(f"Fixed: {fixed}")
    total += fixed[len(fixed) // 2]

print(f"Part 2:", total)
