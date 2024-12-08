file = open("easy.txt", "r")

lines = file.readlines()
total = 0


def is_safe(report):
    diffs = []
    for i in range(1, len(report)):
        diffs.append(report[i] - report[i - 1])
        if abs(report[i] - report[i - 1]) >= 4:
            return False
    for diff in diffs:
        if diff == 0:
            return False
    if diffs[0] > 0 and not all(x > 0 for x in diffs):
        return False
    if diffs[0] < 0 and not all(x < 0 for x in diffs):
        return False
    return True


for line in lines:
    nums = [int(x) for x in line.strip().split()]
    if is_safe(nums):
        total += 1

print("Part 1: ", total)

total = 0

for line in lines:
    nums = [int(x) for x in line.strip().split()]
    safe = False
    if is_safe(nums):
        safe = True
    else:
        for i in range(len(nums)):
            num_copy = nums.copy()
            del num_copy[i]
            cur_safe = is_safe(num_copy)
            if cur_safe:
                print(f"List {nums} is safe if we remove number {nums[i]}")
                safe = True
                break
    if safe:
        total += 1
    else:
        print(f"List {nums} is not safe no matter what we do!")

print("Part 2: ", total)