
import os
os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from intcode.IntcodeComputer import IntcodeComputer

def run_program(instructions, run_mode):
    def get_input():
        return run_mode
    p = IntcodeComputer(instructions, get_input)
    print(p.run())


def solve_part_1(instructions):
    run_program(instructions, 1)


def solve_part_2(instructions):
    run_program(instructions, 2)


def main():
    moons = {}
    with open('input.txt') as f:
        in_data = list(map(int, f.read().strip().split(",")))
        print('Part 1: ', end='')
        solve_part_1(in_data)
        print('Part 2: ', end='')
        solve_part_2(list(in_data))

if __name__ == "__main__":
    main()