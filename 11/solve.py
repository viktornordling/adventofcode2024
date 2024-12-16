file = open("input.txt", "r")

lines = file.readlines()

total = 0

line = lines[0]

nums = [int(x) for x in line.split()]


def blink(nums):
    result = []
    for num in nums:
        if type(num) == str:
            result.append(num)
            continue
        if num == 0:
            result.append(1)
        elif len(str(num)) % 2 == 0:
            num_as_str = str(num)
            first = num_as_str[0:len(num_as_str) // 2]
            second = num_as_str[(len(num_as_str) // 2):]
            result.append(int(first))
            result.append(int(second))
        else:
            result.append(num * 2024)
    return result


last = 0

num_to_expansions = {}
total_iterations = 75
precalced_iterations = 38

for i in range(10):
    low_nums = [i]
    num_to_expansions[i] = []
    for j in range(precalced_iterations):
        print(f"i = {i}, j = {j}")
        last = len(low_nums)
        low_nums = blink(low_nums)
        # print(f"i = {i}, len = {len(low_nums)}")
        num_to_expansions[i].append(f"{len(low_nums)}: not needed")
        # print(nums)

# print(num_to_expansions)

precalc = True

for i in range(total_iterations):
    print(f"i = {i}")
    last = len(nums)
    nums = blink(nums)
    print(f"len = {len(nums)}, last = {last}, diff = {len(nums) - last}")
    # if False:
    if i >= precalced_iterations and precalc:
        remaining = total_iterations - i - 1
        if remaining == 0:
            break
        new = []
        for num in nums:
            if type(num) == str:
                new.append(num)
                continue
            if num > 9:
                new.append(num)
            else:
                expansions = num_to_expansions[num]
                new.append(f"{expansions[remaining - 1]}")
        nums = new
        # print(f"new = {new}, nums = {nums}")

total = 0
# print(f"nums = {nums}")
for num in nums:
    if type(num) == int:
        total += 1
    else:
        total += int(num.split(":")[0])

print("Part 2:", total)
