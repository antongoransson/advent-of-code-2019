import os
os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from intcode.IntcodeComputer import IntcodeComputer


def run_program(instructions, grid, coins=None):
    def get_input():
        return joystick
    program = IntcodeComputer(instructions, get_input)
    score = 0
    x, y = None, None
    brick_x = 21
    joystick = 0
    if coins != None:
        program.set_val(0, coins)
    while not program.done:
        x = program.run()
        y = program.run()
        if x == -1 and y == 0:
            score = program.run()
        else:
            out = program.run()
            if out == 4:
                if x < brick_x:
                    joystick = -1
                elif x > brick_x:
                    joystick = 1
                else:
                    joystick = 0
                brick_x += joystick
            grid[x, y] = out
    return score


def solve_part_1(instructions):
    grid = {}
    run_program(instructions, grid)
    return len([v for v in grid.values() if v == 2])


def solve_part_2(instructions):
    return run_program(instructions, {}, 2)


def main():
    with open('input.txt') as f:
        in_data = list(map(int, f.read().strip().split(",")))
        sol1 = solve_part_1(in_data)
        print('Part 1: {}'.format(sol1))
        sol2 = solve_part_2(in_data)
        print('Part 2: {}'.format(sol2))


if __name__ == "__main__":
    main()
