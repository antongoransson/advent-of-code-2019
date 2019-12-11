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
    # print(a)
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
    4: output,
    5: jmpift,
    6: jmpiff,
    7: less,
    8: eq
}

directions = {
    0: (-1, 0),
    1: (0, 1),
    2: (1, 0),
    3: (0, -1),
}
dx = {
    0: -1,
    1: 0,
    2: 1,
    3: 0
}
dy = {
    0: 0,
    1: 1,
    2: 0,
    3: -1
}


def run_program(program, grid, start_val):
    ip, rel_base = 0, 0
    d = 0
    x, y = 0, 0
    seen = set()
    color = None
    grid[x, y] = start_val
    while program[ip] != 99:
        params = (str(program[ip])[:-2]).zfill(3)
        op = int(str(program[ip])[-2:])
        p_modes = list(map(int, params))[::-1]
        if op == 3:
            seen.add((x, y))
            val = grid[x, y]
            ip = write(program, ip, val, p_modes, rel_base)
        elif op == 4:
            ip, out = output(program, ip, p_modes, rel_base)
            if color == None:
                color = out
                grid[x, y] = color
            else:
                if out == 0:
                    d = (d - 1) % 4
                elif out == 1:
                    d = (d + 1) % 4
                x += dx[d]
                y += dy[d]
                color = None
        elif op == 9:
            rel_base = adj_rel_base(program, ip, p_modes, rel_base)
            ip += 2
        else:
            ip = op_codes[op](program, ip, p_modes, rel_base)
    return len(seen)


def solve_part_1(program):
    memory = defaultdict(int)
    for i, x in enumerate(program):
        memory[i] = x
    grid = defaultdict(int)
    return run_program(memory, grid, 0)


def solve_part_2(program):
    memory = defaultdict(int)
    for i, x in enumerate(program):
        memory[i] = x
    grid = defaultdict(int)
    hull = [['.' for _ in range(43)] for _ in range(6)]
    run_program(memory, grid, 1)
    for (x, y), v in grid.items():
        hull[x][y] = '.' if v == 0 else '#'
    for row in hull:
        print("".join(row))


def main():
    with open('input.txt') as f:
        in_data = list(map(int, f.read().strip().split(",")))
        sol1 = solve_part_1(in_data)
        print('Part 1: {}'.format(sol1))
        print('Part 2: ')
        solve_part_2(in_data)


if __name__ == "__main__":
    main()
