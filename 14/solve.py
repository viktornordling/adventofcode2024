import os
from time import sleep

file = open("input.txt", "r")

lines = file.readlines()

total = 0

cells = {}
all_robots = []

for line in lines:
    robot_parts = line.split(" ")
    pos = [int(x) for x in robot_parts[0].split("=")[1].split(",")]
    vel = [int(x) for x in robot_parts[1].split("=")[1].split(",")]
    pos_pair = (pos[0], pos[1])
    vel_pair = (vel[0], vel[1])
    all_robots.append((pos_pair, vel_pair))

cols = 101
rows = 103


def should_print_cells():
    return True
    # empties = 0
    # for y in range(rows):
    #     for x in range(cols):
    #         cur = cells.get((x, y), [])
    #         if len(cur) == 0:
    #             empties += 1
    # return empties > 2000


def print_cells(i):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Iterations:", i)
    for y in range(rows):
        for x in range(cols):
            cur = cells.get((x, y), [])
            intensity = len(cur)
            if intensity == 0:
                print(".", end="")
            else:
                if intensity < 10:
                    car = f"{intensity}"
                elif intensity == 10:
                    car = 'A'
                elif intensity == 12:
                    car = 'B'
                elif intensity == 13:
                    car = 'C'
                elif intensity == 14:
                    car = 'D'
                elif intensity == 15:
                    car = 'E'
                elif intensity == 16:
                    car = 'F'
                elif intensity > 16:
                    car = 'G'
                else:
                    car = '#'
                print(car, end="")
        print()


for i in range(1000000):
    new_robots = []
    for robot in all_robots:
        cur_pos = robot[0]
        vel = robot[1]
        new_pos = ((cur_pos[0] + vel[0]) % cols, (cur_pos[1] + vel[1]) % rows)
        # print(new_pos)
        new_robots.append((new_pos, vel))
    all_robots = new_robots

    cells = {}
    for robot in all_robots:
        # print(f"robot {robot} is in position {robot[0]}")
        pos_pair = robot[0]
        robots = cells.get(pos_pair, [])
        robots.append(pos_pair)
        cells[pos_pair] = robots
    if i > 6440:
        print_cells(i + 1)
        sleep(1)




# Count the robots in each quadrant
top_left = 0
bottom_left = 0
top_right = 0
bottom_right = 0


for y in range(rows):
    for x in range(cols):
        robots = cells.get((x, y), [])
        if len(robots) == 0:
            stuff = True
            # print(".", end='')
        else:
            mid_x = cols // 2
            mid_y = rows // 2
            rob_x = x
            rob_y = y
            # print(f"mid_x = {mid_x}, mid_y = {mid_y}, x = {x}, y = {y}")
            # print(f"rob_x = {rob_x}, rob_y = {rob_y}")
            if rob_x < mid_x and rob_y < mid_y:
                top_left += len(robots)
            if rob_x < mid_x and rob_y >= mid_y + 1:
                bottom_left += len(robots)
            if rob_x >= mid_x + 1 and rob_y < mid_y:
                top_right += len(robots)
            if rob_x >= mid_x + 1 and rob_y >= mid_y + 1:
                # print("increasing bottom right")
                bottom_right += len(robots)
            # print(len(robots), end='')
    # print()

print(f"top_left = {top_left}, top_right = {top_right}, bottom_left = {bottom_left}, bottom_right = {bottom_right}")
print("Part 1:", top_left * top_right * bottom_left * bottom_right)
