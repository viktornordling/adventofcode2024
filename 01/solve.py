from collections import Counter

file = open("easy.txt", "r")
total = 0
list1 = []
list2 = []
lines = file.readlines()
for line in lines:
    nums = [int(x) for x in line.strip().split()]
    list1.append(nums[0])
    list2.append(nums[1])

list1.sort()
list2.sort()

for i in range(0, len(lines)):
    print(abs(list1[i] - list2[i]))
    total += abs(list1[i] - list2[i])

print("Part 1: ", total)

freqs = Counter(list2)

total = 0

for i in range(0, len(lines)):
    num = list1[i]
    freq = freqs[num]
    print(num * freq)
    total += num * freq

print("Part 2: ", total)