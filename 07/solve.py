import itertools

file = open("input.txt", "r")

lines = file.readlines()

total = 0


def calc(nums, ops):
    result = nums[0]
    for i in range(1, len(nums)):
        if ops[i - 1] == '+':
            result += nums[i]
        elif ops[i - 1] == '*':
            result *= nums[i]
        elif ops[i - 1] == '|':
            result = int(str(result) + str(nums[i]))
    return result


def calc_with_conc(nums, ops):
    result = nums[0]
    for i in range(1, len(nums)):
        if ops[i - 1] == '+':
            result += nums[i]
        elif ops[i - 1] == '*':
            result *= nums[i]
        elif ops[i - 1] == '|':
            # print(f"found |, cur = {result}, nums[i] = {nums[i]}")
            result = int(str(result) + str(nums[i]))
            # print(f"found |, cur now = {result}")
    return result


for line in lines:
    parts = line.split(":")
    result = int(parts[0])
    nums = [int(x) for x in parts[1].split()]

    i = 0
    permutations = list(itertools.product(['+', '*'], repeat=len(nums) - 1))
    possible = False
    for permutation in permutations:
        if calc(nums, permutation) == result:
            possible = True
            break
    if possible:
        total += result


print("Part 1:", total)


total = 0

for line in lines:
    parts = line.split(":")
    result = int(parts[0])
    nums = [int(x) for x in parts[1].split()]

    i = 0
    permutations = list(itertools.product(['+', '*', '|'], repeat=len(nums) - 1))
    possible = False
    for permutation in permutations:
        if calc_with_conc(nums, permutation) == result:
            print(f"{result} can be made with operators {permutation}")
            possible = True
            break
    if possible:
        total += result

print("Part 2:", total)
