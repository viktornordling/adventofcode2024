import re

input_string = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

pattern = r'mul\((\d+),(\d+)\)|do\(\)|don\'t\(\)'

mul_enabled = True
total_sum = 0

actions = re.finditer(pattern, input_string)

for action in actions:
    if action.group(0) == "do()":
        mul_enabled = True
    elif action.group(0) == "don't()":
        mul_enabled = False
    elif action.group(0).startswith("mul"):
        if mul_enabled:
            x = int(action.group(1))
            y = int(action.group(2))
            total_sum += x * y

print(total_sum)