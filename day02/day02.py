from itertools import combinations


def addr(a, b, c, registers):
    registers[int(c)] = registers[int(a)] + registers[int(b)]
    return registers[int(c)]


def mulr(a, b, c, registers):
    registers[int(c)] = registers[int(a)] * registers[int(b)]
    return registers[int(c)]


op_codes = {
    1: addr,
    2: mulr,
}


def solve_part_1(registers):
    i = 0
    registers[1] = 12
    registers[2] = 2
    while registers[i] != 99:
        a = registers[i + 1]
        b = registers[i + 2]
        c = registers[i + 3]
        op_codes[registers[i]](a, b, c, registers)
        i += 4
    return registers[0]


def solve_part_2(default_state):
    test_range = [i for i in range(100)]
    for x, y in combinations(test_range, 2):
        registers = list(default_state)
        registers[1] = x
        registers[2] = y
        i = 0
        while registers[i] != 99:
            a = registers[i + 1]
            b = registers[i + 2]
            c = registers[i + 3]
            op_codes[registers[i]](a, b, c, registers)
            i += 4
        if registers[0] == 19690720:
            return registers[1] * 100 + registers[2]


def main():
    with open('input.txt') as f:
        in_data = list((map(int, f.read().strip().split(","))))
        sol1 = solve_part_1(list(in_data))
        print('Part 1: {}'.format(sol1))
        sol2 = solve_part_2(in_data)
        print('Part 2: {}'.format(sol2))


if __name__ == "__main__":
    main()
