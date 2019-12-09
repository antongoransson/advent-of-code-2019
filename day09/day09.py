from itertools import combinations, permutations
from collections import defaultdict

POS_MODE = 0
IMM_MODE = 1
PARAM_MODE = 2


def addr(registers, ip, imm1, imm2, imm3, rel_base):
    a, b, c = registers[ip + 1], registers[ip + 2], registers[ip + 3]
    if imm1 == POS_MODE:
        a = registers[a]
    elif imm1 == PARAM_MODE:
        a = registers[rel_base + a]
    if imm2 == POS_MODE:
        b = registers[b]
    elif imm2 == PARAM_MODE:
        b = registers[rel_base + b]
    if imm3 == PARAM_MODE:
        c = rel_base + c
    registers[c] = a + b
    ip += 4
    return ip


def mulr(registers, ip, imm1, imm2, imm3, rel_base):
    a, b, c = registers[ip + 1], registers[ip + 2], registers[ip + 3]
    if imm1 == POS_MODE:
        a = registers[a]
    if imm2 == POS_MODE:
        b = registers[b]
    if imm1 == PARAM_MODE:
        a = registers[rel_base + a]
    if imm2 == PARAM_MODE:
        b = registers[rel_base + b]
    if imm3 == PARAM_MODE:
        c = rel_base + c
    registers[c] = a * b
    ip += 4
    return ip


def write(registers, ip,  val1, imm1, rel_base):
    a = registers[ip + 1]
    if imm1 == PARAM_MODE:
        a = rel_base + a
    registers[a] = val1
    ip += 2
    return ip


def output(registers, ip, imm1, rel_base):
    a = registers[ip + 1]
    if imm1 == POS_MODE:
        a = registers[a]
    if imm1 == PARAM_MODE:
        a = registers[rel_base + a]
    print(a)
    ip += 2
    return ip


def jmpift(registers, ip, imm1, imm2, imm3, rel_base):
    a, b = registers[ip + 1], registers[ip + 2]
    if imm1 == POS_MODE:
        a = registers[a]
    if imm2 == POS_MODE:
        b = registers[b]
    if imm1 == PARAM_MODE:
        a = registers[rel_base + a]
    if imm2 == PARAM_MODE:
        b = registers[rel_base+b]
    ip = ip + 3 if a == 0 else b
    return ip


def jmpiff(registers, ip, imm1, imm2, imm3, rel_base):
    a, b = registers[ip + 1], registers[ip + 2]
    if imm1 == POS_MODE:
        a = registers[a]
    if imm2 == POS_MODE:
        b = registers[b]
    if imm1 == PARAM_MODE:
        a = registers[rel_base + a]
    if imm2 == PARAM_MODE:
        b = registers[rel_base+b]
    ip = ip + 3 if a != 0 else b
    return ip


def less(registers, ip, imm1, imm2, imm3, rel_base):
    a, b, c = registers[ip + 1], registers[ip + 2], registers[ip + 3]
    if imm1 == POS_MODE:
        a = registers[a]
    if imm2 == POS_MODE:
        b = registers[b]
    if imm1 == PARAM_MODE:
        a = registers[rel_base + a]
    if imm2 == PARAM_MODE:
        b = registers[rel_base+b]
    if imm3 == PARAM_MODE:
        c = rel_base + c
    registers[c] = int(a < b)
    ip += 4
    return ip


def eq(registers, ip, imm1, imm2, imm3, rel_base):
    a, b, c = registers[ip + 1], registers[ip + 2], registers[ip + 3]
    if imm1 == POS_MODE:
        a = registers[a]
    if imm2 == POS_MODE:
        b = registers[b]
    if imm1 == PARAM_MODE:
        a = registers[rel_base + a]
    if imm2 == PARAM_MODE:
        b = registers[rel_base + b]
    if imm3 == PARAM_MODE:
        c = rel_base + c
    registers[c] = int(a == b)
    ip += 4
    return ip


def adj_rel_base(registers, ip, imm1, rel_base):
    a = registers[ip + 1]
    if imm1 == POS_MODE:
        a = registers[a]
    if imm1 == PARAM_MODE:
        a = registers[rel_base + a]
    rel_base += a
    return rel_base


op_codes = {
    1: addr,
    2: mulr,
    5: jmpift,
    6: jmpiff,
    7: less,
    8: eq,
    9: adj_rel_base
}


def run_program(program, run_mode):
    ip, rel_base = 0, 0
    while program[ip] != 99:
        op = program[ip]
        params = (str(op)[:-2]).zfill(3)
        op = int(str(op)[-2:])
        imm3, imm2, imm1 = map(int, params)
        if op == 3:
            ip = write(program, ip, run_mode, imm1, rel_base)
        elif op == 4:
            ip = output(program, ip, imm1, rel_base)
        elif op == 9:
            rel_base = adj_rel_base(program, ip, imm1, rel_base)
            ip += 2
        else:
            ip = op_codes[op](program, ip, imm1, imm2, imm3, rel_base)
    return


def solve_part_1(program):
    memory = {i: x for i, x in enumerate(program)}
    a = run_program(memory, 1)


def solve_part_2(program):
    memory = {i: x for i, x in enumerate(program)}
    a = run_program(memory, 2)


def main():
    with open('input.txt') as f:
        in_data = list(map(int, f.read().strip().split(",")))
        sol1 = solve_part_1(in_data)
        print('Part 1: {}'.format(sol1))
        sol2 = solve_part_2(list(in_data))
        print('Part 2: {}'.format(sol2))


if __name__ == "__main__":
    main()
