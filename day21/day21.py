import os
os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from intcode.IntcodeComputer import IntcodeComputer


def to_ascii(s):
    return [(ord(c)) for c in s] + [ord("\n")]

def solve_part_1(instructions):
    spring_code = [
        "NOT A T",
        "NOT B J",
        "OR T J",
        "NOT C T",
        "OR T J",
        "AND D J",
        "WALK"
    ]
    spring_code_ascii = to_ascii("\n".join(spring_code))

    def get_input():
        return spring_code_ascii.pop(0)
    program = IntcodeComputer(instructions, get_input)
    while not program.done:
        c = program.run()
    return c

def solve_part_2(instructions):
    spring_code = [
        "NOT A T",
        "NOT B J",
        "OR T J",
        "NOT C T",
        "OR T J",
        "AND D J",
        "NOT E T",
        "NOT T T",
        "OR H T",
        "AND T J",
        "RUN"
    ]
    spring_code_ascii = to_ascii("\n".join(spring_code))

    def get_input():
        return spring_code_ascii.pop(0)
        
    program = IntcodeComputer(instructions, get_input)
    while not program.done:
        c = program.run()
    return c


def main():
    with open('input.txt') as f:
        data = list(map(int, f.read().strip().split(",")))
    sol1 =  solve_part_1(data)
    print('Part 1: {}'.format(sol1))
    sol2 = solve_part_2(data)
    print('Part 2: {}'.format(sol2))


if __name__ == "__main__":
    main()
