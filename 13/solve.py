from pulp import LpProblem, LpVariable, LpMinimize, GLPK
import numpy as np

lines = open('input.txt', 'r').read()
test_cases = lines.split("\n\n")


def find_cost_to_win_prize(a_x, a_y, b_x, b_y, goal_x, goal_y):
    cheapest = 100000
    for i in range(100):
        cur_x = i * a_x
        cur_y = i * a_y
        if cur_x == goal_x and cur_y == goal_y:
            if 3 * i< cheapest:
                cheapest = 3 * i
        for j in range(100):
            cur_x += b_x
            cur_y += b_y
            if cur_x == goal_x and cur_y == goal_y:
                if 3 * i + j < cheapest:
                    cheapest = 3 * i + (j + 1)
    if cheapest < 100000:
        return cheapest
    else:
        return 0


def find_cost_to_win_prize_with_cramer(a_x, a_y, b_x, b_y, goal_x, goal_y):
    matrix_a = [[a_x, b_x], [a_y, b_y]]
    matrix_a_1 = [[goal_x, b_x], [goal_y, b_y]]
    matrix_a_2 = [[a_x, goal_x], [a_y, goal_y]]

    a_det = np.linalg.det(matrix_a)
    a1_det = np.linalg.det(matrix_a_1)
    a2_det = np.linalg.det(matrix_a_2)

    a = int(round(a1_det / a_det))
    b = int(round(a2_det / a_det))

    # Check that it worked out.
    real_x = a * a_x + b * b_x
    real_y = a * a_y + b * b_y

    if real_x == goal_x and real_y == goal_y:
        print("That worked!")
        return a * 3 + b
    return 0


def find_cost_to_win_prize_with_pulp(a_x, a_y, b_x, b_y, goal_x, goal_y):
    model = LpProblem(name="my-problem", sense=LpMinimize)

    a_presses = LpVariable(name="a", lowBound=0, cat="Integer")
    b_presses = LpVariable(name="b", lowBound=0, cat="Integer")

    # expression = a_presses * a_x + b_presses * b_x == goal_x and a_presses * a_y + b_presses * b_y == goal_y
    constraint_1 = a_presses * a_x + b_presses * b_x == goal_x
    constraint_2 = a_presses * a_y + b_presses * b_y == goal_y

    constraint_3 = a_presses * a_x + b_presses * b_x <= goal_x + 1000
    constraint_4 = a_presses * a_y + b_presses * b_y <= goal_y + 1000

    print("const", type(constraint_1))
    print("const", type(constraint_2))

    model += a_presses * 3 + b_presses
    model += constraint_1
    model += constraint_2
    model += constraint_3
    model += constraint_4
    # print(model.objective.value())

    status = model.solve(solver=GLPK(msg=False))
    print("Status:", status)
    if status == 1:
        return int(model.objective.value())
    return 0


total = 0
total_2 = 0

for test_case in test_cases:
    lines = test_case.split("\n")
    button_a_props = lines[0].split("+")
    button_b_props = lines[1].split("+")
    goal = lines[2].split("=")
    a_x = int(button_a_props[1].split(",")[0])
    a_y = int(button_a_props[2])
    b_x = int(button_b_props[1].split(",")[0])
    b_y = int(button_b_props[2])
    goal_x = int(goal[1].split(",")[0])
    goal_y = int(goal[2])
    print(button_a_props)
    print(button_b_props)
    print(goal)

    cheapest = find_cost_to_win_prize(a_x, a_y, b_x, b_y, goal_x, goal_y)
    # cheapest_2 = find_cost_to_win_prize_with_pulp(a_x, a_y, b_x, b_y, goal_x + 10000000000000, goal_y + 10000000000000)
    cheapest_with_cramer = find_cost_to_win_prize_with_cramer(a_x, a_y, b_x, b_y, goal_x + 10000000000000, goal_y + 10000000000000)
    total_2 += cheapest_with_cramer
    print(cheapest)
    total += cheapest

print("Part 1:", total, total_2)

