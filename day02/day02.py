from itertools import combinations


def addr(a, b, c, registers):
    registers[int(c)] = registers[int(a)] + registers[int(b)]


def mulr(a, b, c, registers):
    registers[int(c)] = registers[int(a)] * registers[int(b)]


op_codes = {
    1: addr,
    2: mulr,
}


def run_program(noun, verb, registers):
    registers[1] = noun
    registers[2] = verb
    i = 0
    while registers[i] != 99:
        op, a, b, c = registers[i:i + 4]
        op_codes[op](a, b, c, registers)
        i += 4
    return registers


def solve_part_1(registers):
    return run_program(12, 2, registers[:])[0]


def solve_part_2(default_state):
    val_range = [i for i in range(100)]
    for x, y in combinations(val_range, 2):
        registers = run_program(x, y, default_state[:])
        if registers[0] == 19690720:
            return registers[1] * 100 + registers[2]


def main():
    with open('input.txt') as f:
        in_data = list(map(int, f.read().strip().split(",")))
        sol1 = solve_part_1(in_data)
        print('Part 1: {}'.format(sol1))
        sol2 = solve_part_2(list(in_data))
        print('Part 2: {}'.format(sol2))


if __name__ == "__main__":
    main()
