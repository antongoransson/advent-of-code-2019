def addr(registers, ip, imm1, imm2, imm3, val=None):
    a, b, c = registers[ip + 1: ip + 4]
    if imm1 == 0:
        a = registers[a]
    if imm2 == 0:
        b = registers[b]
    registers[c] = a + b
    ip += 4
    return ip


def mulr(registers, ip, imm1, imm2, imm3, val=None):
    a, b, c = registers[ip + 1: ip + 4]
    if imm1 == 0:
        a = registers[a]
    if imm2 == 0:
        b = registers[b]
    registers[c] = a * b
    ip += 4
    return ip


def write(registers, ip, imm1, imm2, imm3, val):
    registers[registers[ip + 1]] = val
    ip += 2
    return ip


def output(registers, ip, imm1, imm2, imm3, val=None):
    print(registers[registers[ip + 1]])
    ip += 2
    return ip


def jmpift(registers, ip, imm1, imm2, imm3, val=None):
    a, b = registers[ip + 1: ip + 3]
    if imm1 == 0:
        a = registers[a]
    if imm2 == 0:
        b = registers[b]
    ip = ip + 3 if a == 0 else b
    return ip


def jmpiff(registers, ip, imm1, imm2, imm3, val=None):
    a, b = registers[ip + 1: ip + 3]
    if imm1 == 0:
        a = registers[a]
    if imm2 == 0:
        b = registers[b]
    ip = ip + 3 if a != 0 else b
    return ip


def less(registers, ip, imm1, imm2, imm3, val=None):
    a, b, c = registers[ip + 1: ip + 4]
    if imm1 == 0:
        a = registers[a]
    if imm2 == 0:
        b = registers[b]
    registers[c] = int(a < b)
    ip += 4
    return ip


def eq(registers, ip, imm1, imm2, imm3, val=None):
    a, b, c = registers[ip + 1: ip + 4]
    if imm1 == 0:
        a = registers[a]
    if imm2 == 0:
        b = registers[b]
    registers[c] = int(a == b)
    ip += 4
    return ip


op_codes = {
    1: addr,
    2: mulr,
    3: write,
    4: output,
    5: jmpift,
    6: jmpiff,
    7: less,
    8: eq
}


def run_program(program, machine_id):
    ip = 0
    ip = write(program, ip, 0, 0, 0, machine_id)
    imm1, imm2, imm3 = 0, 0, 0
    while program[ip] != 99:
        op = program[ip]
        params = (str(op)[:-2]).zfill(3)
        op = int(str(op)[-2:])
        imm3, imm2, imm1 = map(int, params)
        ip = op_codes[op](program, ip, imm1, imm2, imm3)


def solve_part_1(program):
    machine_id = 1
    return run_program(program[:], machine_id)


def solve_part_2(program):
    machine_id = 5
    return run_program(program[:], machine_id)


def main():
    with open('input.txt') as f:
        in_data = list(map(int, f.read().strip().split(",")))
        # print(in_data)
        sol1 = solve_part_1(in_data)
        print('Part 1: ^')
        sol2 = solve_part_2(list(in_data))
        print('Part 2: ^')


if __name__ == "__main__":
    main()
