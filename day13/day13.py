from collections import defaultdict
import regex as re

POS_MODE = 0
IMM_MODE = 1
REL_MODE = 2


def get_val(ip, registers, p_mode, rel_base):
    r = registers[ip]
    if p_mode == POS_MODE:
        r = registers[r]
    elif p_mode == REL_MODE:
        r = registers[rel_base + r]
    return r


def addr(registers, ip, p_modes, rel_base):
    a = get_val(ip + 1, registers, p_modes[0], rel_base)
    b = get_val(ip + 2, registers, p_modes[1], rel_base)
    c = registers[ip + 3]
    if p_modes[2] == REL_MODE:
        c = rel_base + c
    registers[c] = a + b
    ip += 4
    return ip


def mulr(registers, ip, p_modes, rel_base):
    a = get_val(ip + 1, registers, p_modes[0], rel_base)
    b = get_val(ip + 2, registers, p_modes[1], rel_base)
    c = registers[ip + 3]
    if p_modes[2] == REL_MODE:
        c = rel_base + c
    registers[c] = a * b
    ip += 4
    return ip


def write(registers, ip,  val1, p_modes, rel_base):
    a = registers[ip + 1]
    if p_modes[0] == REL_MODE:
        a = rel_base + a
    registers[a] = val1
    ip += 2
    return ip


def output(registers, ip, p_modes, rel_base):
    a = get_val(ip + 1, registers, p_modes[0], rel_base)
    ip += 2
    return ip, a


def jmpift(registers, ip, p_modes, rel_base):
    a = get_val(ip + 1, registers, p_modes[0], rel_base)
    b = get_val(ip + 2, registers, p_modes[1], rel_base)
    ip = ip + 3 if a == 0 else b
    return ip


def jmpiff(registers, ip, p_modes, rel_base):
    a = get_val(ip + 1, registers, p_modes[0], rel_base)
    b = get_val(ip + 2, registers, p_modes[1], rel_base)
    ip = ip + 3 if a != 0 else b
    return ip


def less(registers, ip, p_modes, rel_base):
    a = get_val(ip + 1, registers, p_modes[0], rel_base)
    b = get_val(ip + 2, registers, p_modes[1], rel_base)
    c = registers[ip + 3]
    if p_modes[2] == REL_MODE:
        c = rel_base + c
    registers[c] = int(a < b)
    ip += 4
    return ip


def eq(registers, ip, p_modes, rel_base):
    a = get_val(ip + 1, registers, p_modes[0], rel_base)
    b = get_val(ip + 2, registers, p_modes[1], rel_base)
    c = registers[ip + 3]
    if p_modes[2] == REL_MODE:
        c = rel_base + c
    registers[c] = int(a == b)
    ip += 4
    return ip


def adj_rel_base(registers, ip, p_modes, rel_base):
    a = get_val(ip + 1, registers, p_modes[0], rel_base)
    rel_base += a
    return rel_base


op_codes = {
    1: addr,
    2: mulr,
    5: jmpift,
    6: jmpiff,
    7: less,
    8: eq
}


def run_program(program, grid, coins=None):
    ip, rel_base = 0, 0
    score = 0
    x, y = None, None
    brick_x = 21
    joystick = 0
    if coins != None:
        program[0] = coins
    while program[ip] != 99:
        params = (str(program[ip])[:-2]).zfill(3)
        op = int(str(program[ip])[-2:])
        p_modes = list(map(int, params))[::-1]
        if op == 3:
            brick_x += joystick
            ip = write(program, ip, joystick, p_modes, rel_base)
        elif op == 4:
            if x == None:
                ip, x = output(program, ip, p_modes, rel_base)
            elif y == None:
                ip, y = output(program, ip, p_modes, rel_base)
            else:
                if x == -1 and y == 0:
                    ip, score = output(program, ip, p_modes, rel_base)
                else:
                    ip, out = output(program, ip, p_modes, rel_base)
                    if out == 4:
                        if x < brick_x:
                            joystick = -1
                        elif x > brick_x:
                            joystick = 1
                        else:
                            joystick = 0
                    grid[x, y] = out
                x, y = None, None
        elif op == 9:
            rel_base = adj_rel_base(program, ip, p_modes, rel_base)
            ip += 2
        else:
            ip = op_codes[op](program, ip, p_modes, rel_base)
    return score


def solve_part_1(program):
    memory = defaultdict(int, {k: v for k, v in enumerate(program)})
    grid = {}
    run_program(memory, grid)
    return len([v for v in grid.values() if v == 2])


def solve_part_2(program):
    memory = defaultdict(int, {k: v for k, v in enumerate(program)})
    score = run_program(memory, {}, 2)
    return score


def main():
    moons = {}
    with open('input.txt') as f:
        in_data = list(map(int, f.read().strip().split(",")))
        sol1 = solve_part_1(in_data)
        print('Part 1: {}'.format(sol1))
        sol2 = solve_part_2(in_data)
        print('Part 2: {}'.format(sol2))


if __name__ == "__main__":
    main()
