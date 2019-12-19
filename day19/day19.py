import os
os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from intcode.IntcodeComputer import IntcodeComputer




def solve_part_1(instructions):
    s = 0
    size = 50
    for y in range(size):
        for x in range(size):
            drones = [x, y]
            def get_input():
                return drones.pop(0)
            program = IntcodeComputer(instructions, get_input)
            o = program.run()
            s += o
    return s

def solve_part_2(instructions):
    x = 0
    y = 0
    def get_input():
        return drones.pop(0)
    while True:
        drones = [x + 99, y - 99]
        program = IntcodeComputer(instructions, get_input)
        if program.run() == 1:
            return x * 10000 + y - 99
        y += 1
        drones = [x, y]
        program = IntcodeComputer(instructions, get_input)
        if program.run() == 0:
            x += 1

def main():
    with open('input.txt') as f:
        data = list(map(int, f.read().strip().split(",")))
    sol1 =  solve_part_1(data)
    print('Part 1: {}'.format(sol1))
    sol2 = solve_part_2(data)
    print('Part 2: {}'.format(sol2))


if __name__ == "__main__":
    main()
