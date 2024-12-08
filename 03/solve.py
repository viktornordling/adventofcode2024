import re

pattern = r"mul\((\d+),(\d+)\)"

file = open("input.txt", "r")

lines = file.readlines()
total = 0

for line in lines:
    matches = re.findall(pattern, line)

    # print(matches)
    for match in matches:
        mul = int(match[0]) * int(match[1])
        total += mul

print("Part 1: ", total)

total = 0


def do_muls(string: str, start, stop):
    sub = string[start:stop]
    matches = re.findall(pattern, sub)

    tot = 0

    # print(matches)
    for match in matches:
        mul = int(match[0]) * int(match[1])
        tot += mul
    return tot


for line in lines:
    parse = True
    index = 0
    while index < len(line):
        if parse:
            stop = line.find("don't()", index)
            total += do_muls(line, index, stop)
            if stop == -1:
                index = len(line) + 1
            else:
                index = stop + 7
                parse = False
        else:
            next_do = line.find("do()", index)
            if next_do == -1:
                index = len(line) + 4
            else:
                index = next_do
                parse = True

print("Part 2: ", total)
