import math

data = open('input.txt', 'r').read()
parts = data.split("\n\n")
register_lines = parts[0].split("\n")
instructions_line = parts[1].split("\n")

result = ""

registers = {
    'A': int(register_lines[0].split()[2]),
    'B': int(register_lines[1].split()[2]),
    'C': int(register_lines[2].split()[2])
}

instructions = [int(x) for x in instructions_line[0].split()[1].split(",")]
output = ""


def get_combo(operand):
    if operand < 4:
        return operand
    elif operand == 4:
        return registers['A']
    elif operand == 5:
        return registers['B']
    elif operand == 6:
        return registers['C']


def adv(pc, operand):
    register = registers['A']
    op_value = get_combo(operand)
    res = int(register // (math.pow(2, op_value)))
    registers['A'] = res
    return pc + 2


def bxl(pc, operand):
    register = registers['B']
    res = register ^ operand
    registers['B'] = res
    return pc + 2


def bst(pc, operand):
    op_value = get_combo(operand)
    res = op_value % 8
    registers['B'] = res
    return pc + 2


def jnz(pc, operand):
    register = registers['A']
    if register == 0:
        return pc + 2
    else:
        return operand


def bxc(pc, operand):
    register_b = registers['B']
    register_c = registers['C']
    res = register_b ^ register_c
    registers['B'] = res
    return pc + 2


def out(pc, operand):
    global output
    op_value = get_combo(operand)
    output += str(op_value % 8) + ','
    return pc + 2


def bdv(pc, operand):
    register = registers['A']
    op_value = get_combo(operand)
    res = int(register // (math.pow(2, op_value)))
    registers['B'] = res
    return pc + 2


def cdv(pc, operand):
    register = registers['A']
    op_value = get_combo(operand)
    res = int(register // (math.pow(2, op_value)))
    registers['C'] = res
    return pc + 2


ops = {
    0: adv,
    1: bxl,
    2: bst,
    3: jnz,
    4: bxc,
    5: out,
    6: bdv,
    7: cdv,
}


def run_program(a_value):
    global output
    registers['A'] = a_value
    pc = 0
    while pc < len(instructions):
        op_code = instructions[pc]
        op = ops[op_code]
        operand = instructions[pc + 1]
        # print("op_code:", op_code, "operand:", operand)
        pc = op(pc, operand)
    return output


goal = ""
for instruction in instructions:
    goal += str(instruction) + ','

op1 = 1
op2 = 6
bits = []
num_bits_in_solution = 48
for i in range(num_bits_in_solution):
    bits.append('0')

locked_in_digits = []
for i in range(num_bits_in_solution):
    locked_in_digits.append('0')


def set_octet(bit_list, locked_in, number_to_set, index_to_set_from):
    # Convert number to set to a 3 bit number (as a binary string).
    number_to_set_as_bitstring = '{0:03b}'.format(number_to_set)
    for j in range(3):
        bit_list[index_to_set_from + j] = number_to_set_as_bitstring[j]
        locked_in[index_to_set_from + j] = 'L'


def solve_digits(a, l, p_index, removed_digits):
    if p_index > 15:
        # We're done, return A.
        return True, a
    p = instructions[p_index]
    num_works = 0
    for j in range(8):
        d = j
        digits_to_remove = d ^ op1
        # Last 3 bits should be (D xor op1) xor (P xor op2).
        last_3_bits_after_removing_d_bits = (d ^ op1) ^ (p ^ op2)
        potential1 = a.copy()
        locked1 = l.copy()
        potential2 = a.copy()
        locked2 = l.copy()
        set_octet(potential1, locked1, d, len(potential1) - 3 - removed_digits)
        set_octet(potential2, locked2, last_3_bits_after_removing_d_bits, len(potential2) - digits_to_remove - 3 - removed_digits)
        # Check if we have any conflicting digits.
        works = True
        l_for_recursing = l.copy()
        a_for_recursing = a.copy()
        for k in range(len(potential1)):
            if locked1[k] == 'L' and locked2[k] == 'L':
                if potential1[k] != potential2[k]:
                    # print(f"{d} does not work.")
                    works = False
                    break
            if locked1[k] == 'L':
                l_for_recursing[k] = 'L'
                a_for_recursing[k] = potential1[k]
            if locked2[k] == 'L':
                l_for_recursing[k] = 'L'
                a_for_recursing[k] = potential2[k]
        if works:
            # print(f"{d} works!")
            num_works += 1
            works, sol = solve_digits(a_for_recursing, l_for_recursing, p_index + 1, removed_digits + 3)
            if works:
                return works, sol
    return False, a


# Part 1:
result = run_program(30899381)
print("Part 1:", result[:-1])

# Part 2:
solved, solution = solve_digits(bits, locked_in_digits, 0, 0)
# For some reason, the first bit in the solution is a 0, but should be a 1.
solution[0] = 1
bit_string = ''.join([str(x) for x in solution])
reg_a = int(bit_string, 2)
print("Part 2:", reg_a)
