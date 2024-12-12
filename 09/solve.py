file = open("input.txt", "r")

lines = file.readlines()

line0 = lines[0]

blocks = []
blocks_2 = []
block_not_free = True
block_id = 0

free_pointer = 0
index = 0

for num in line0:
    num = int(num)
    if block_not_free:
        for i in range(num):
            index += 1
            blocks.append(block_id)
            blocks_2.append(block_id)
        block_id += 1
        block_not_free = False
    else:
        for i in range(num):
            index += 1
            blocks.append(".")
            blocks_2.append(".")
            if free_pointer == 0:
                free_pointer = index - 1
        block_not_free = True

# print(blocks)
# print(f"first free = {free_pointer}")

end_pointer = index - 1
while free_pointer < end_pointer:
    temp = blocks[free_pointer]
    blocks[free_pointer] = blocks[end_pointer]
    blocks[end_pointer] = temp
    free_pointer += 1

    while free_pointer < len(blocks) and blocks[free_pointer] != ".":
        free_pointer += 1
    end_pointer -= 1
    while end_pointer >= 0 and blocks[end_pointer] == ".":
        end_pointer -= 1

# print("Defragged blocks:", blocks)

total = 0

for i, num in enumerate(blocks):
    if num == '.':
        continue
    total += int(num) * i

print("Part 1:", total)


in_free = False
free_size = 0
free_start = 0
# dict where key is size of the free block and the value is a list of indices of start points for free blocks of that size
size_to_index = {}
file_to_index = {}
blocks_2.append(".")

for i, num in enumerate(blocks_2):
    if num == '.' and not in_free:
        in_free = True
        free_size = 1
        free_start = i
    elif num == '.' and in_free:
        free_size += 1
    elif num != "." and in_free:
        # end of free block, store pointer to beginning of block
        indices = []
        if free_size in size_to_index:
            indices = size_to_index[free_size]
        indices.append(free_start)
        size_to_index[free_size] = indices
        in_free = False

# print(size_to_index)

in_file = False
file_size = 0
file_start = -1
file_id = -1
files = []

for i, num in enumerate(blocks_2):
    if num != '.' and not in_file:
        in_file = True
        file_id = num
        file_size = 1
        file_start = i
    elif (num != '.' and num == file_id) and in_file:
        file_size += 1
    elif (num == "." or num != file_id) and in_file:
        # end of file block, store the file block in the list of files as a (file_id, start_pos, size) triad
        files.append((file_id, file_start, file_size))
        file_size = 0
        in_file = False
        # if this immediately starts another file, init the new file here (so ugly)
        if num != ".":
            in_file = True
            file_id = num
            file_size = 1
            file_start = i
del blocks_2[-1]

# print(f"Blocks: {blocks_2}")
# print(f"Files: {files}")
# print(f"Size to index: {size_to_index}")

file_index = 0

files.reverse()
max_free = max(size_to_index.keys())

for file in files:
    # print(f"size_to_index[1] = ", size_to_index[1])
    # print(f"Moving file {file} to the first location that fits.")
    # print("Blocks:", blocks_2)
    file_id, file_start, file_size = file
    # print(f"file_size = {file_size}, max_free = {max_free}")
    min_free_index = len(blocks)
    min_free_list = []
    min_free_index_index = -1
    free_size_to_use = -1
    for free_size in range(file_size, max_free + 1):
        fits = size_to_index.get(free_size, [])
        for g, fit in enumerate(fits):
            if fit < min_free_index:
                min_free_index = fit
                min_free_list = fits
                min_free_index_index = g
                free_size_to_use = free_size
    if min_free_index < file_start:
        # print(f"Move file {file_id} to index {min_free_index}")
        for i in range(min_free_index, min_free_index + file_size):
            blocks_2[i] = file_id
        for i in range(file_start, file_start + file_size):
            blocks_2[i] = '.'
        # Delete the free block as it's no longer free
        new_free = free_size_to_use - file_size
        del min_free_list[min_free_index_index]
        size_to_index[free_size_to_use] = min_free_list
        # Add the new free block
        if new_free > 0:
            frees = size_to_index.get(new_free, [])
            frees.append(min_free_index + file_size)
            size_to_index[new_free] = frees

# print("Final:", blocks_2)

total = 0

for i, num in enumerate(blocks_2):
    if num == '.':
        continue
    total += int(num) * i

print(f"Part 2:", total)