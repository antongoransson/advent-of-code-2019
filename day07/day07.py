from itertools import combinations, permutations


def addr(registers, ip, imm1, imm2, imm3):
    a, b, c = registers[ip + 1: ip + 4]
    if imm1 == 0:
        a = registers[a]
    if imm2 == 0:
        b = registers[b]
    registers[c] = a + b
    ip += 4
    return ip


def mulr(registers, ip, imm1, imm2, imm3):
    a, b, c = registers[ip + 1: ip + 4]
    if imm1 == 0:
        a = registers[a]
    if imm2 == 0:
        b = registers[b]
    registers[c] = a * b
    ip += 4
    return ip


def write(registers, ip,  val1):
    registers[registers[ip + 1]] = val1
    ip += 2
    return ip


def output(registers, ip, outputs, amp):
    outputs[amp] = registers[registers[ip + 1]]
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


def jmpiff(registers, ip, imm1, imm2, imm3, val1=None, val2=None):
    a, b = registers[ip + 1: ip + 3]
    if imm1 == 0:
        a = registers[a]
    if imm2 == 0:
        b = registers[b]
    ip = ip + 3 if a != 0 else b
    return ip


def less(registers, ip, imm1, imm2, imm3, val1=None, val2=None):
    a, b, c = registers[ip + 1: ip + 4]
    if imm1 == 0:
        a = registers[a]
    if imm2 == 0:
        b = registers[b]
    registers[c] = int(a < b)
    ip += 4
    return ip


def eq(registers, ip, imm1, imm2, imm3, val1=None, val2=None):
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
    5: jmpift,
    6: jmpiff,
    7: less,
    8: eq
}


def run_program(program, phases, outputs, amp):
    ip = 0
    ip = write(program, ip, phases[amp])
    while program[ip] != 99:
        op = program[ip]
        params = (str(op)[:-2]).zfill(3)
        op = int(str(op)[-2:])
        imm3, imm2, imm1 = map(int, params)
        if op == 3:
            ip = write(program, ip, outputs[amp - 1])
        elif op == 4:
            ip = output(program, ip, outputs, amp)
        else:
            ip = op_codes[op](program, ip, imm1, imm2, imm3)
    return outputs[amp]


def solve_part_1(program):
    b = []
    for c in permutations([0, 1, 2, 3, 4], 5):
        outputs = [0] * 5
        phases = dict(zip([0, 1, 2, 3, 4], c))
        b.append([run_program(program[:], phases, outputs, amp)
                  for amp in range(0, 5)][-1])
    return max(b)


def solve_part_2(program):
    b = []
    for c in permutations([5, 6, 7, 8, 9], 5):
        outputs = [0] * 5
        phases = dict(zip([0, 1, 2, 3, 4], c))
        b.append([run_program(program[:], phases, outputs, amp)
                  for amp in range(0, 5)][-1])
    return max(b)


def main():
    with open('example2.txt') as f:
        # with open('example.txt') as f:
        in_data = list(map(int, f.read().strip().split(",")))
        # print(in_data)
        # sol1 = solve_part_1(in_data)
        # print('Part 1: {}'.format(sol1))
        sol2 = solve_part_2(list(in_data))
        print('Part 2: {}'.format(sol2))


if __name__ == "__main__":
    main()
