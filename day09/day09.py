from collections import defaultdict

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
    print(a)
    ip += 2
    return ip


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
    4: output,
    5: jmpift,
    6: jmpiff,
    7: less,
    8: eq
}


def run_program(program, run_mode):
    ip, rel_base = 0, 0
    while program[ip] != 99:
        params = (str(program[ip])[:-2]).zfill(3)
        op = int(str(program[ip])[-2:])
        p_modes = list(map(int, params))[::-1]
        if op == 3:
            ip = write(program, ip, run_mode, p_modes, rel_base)
        elif op == 9:
            rel_base = adj_rel_base(program, ip, p_modes, rel_base)
            ip += 2
        else:
            ip = op_codes[op](program, ip, p_modes, rel_base)
    return


def solve_part_1(program):
    memory = defaultdict(int, {k: v for k, v in enumerate(program)})
    run_program(memory, 1)


def solve_part_2(program):
    memory = defaultdict(int, {k: v for k, v in enumerate(program)})
    run_program(memory, 2)


def main():
    with open('input.txt') as f:
        in_data = list(map(int, f.read().strip().split(",")))
        print('Part 1: ', end='')
        solve_part_1(in_data)
        print('Part 2: ', end='')
        solve_part_2(list(in_data))


if __name__ == "__main__":
    main()
