import math

data = open('easy.txt', 'r').read()
parts = data.split("\n\n")
register_lines = parts[0].split("\n")
instructions_line = parts[1].split("\n")

result = ""

registers = {
    'A': int(register_lines[0].split()[2]),
    'B': int(register_lines[0].split()[2]),
    'C': int(register_lines[0].split()[2])
}

instructions = [int(x) for x in instructions_line[0].split()[1].split(",")]

# pc = 0
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
    output += str(op_value) + ','
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
        print("op_code:", op_code, "operand:", operand)
        pc = op(pc, operand)
    print(output)
    output = ""


run_program(729)
