import os
os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from intcode.IntcodeComputer import IntcodeComputer


def run_program(instructions):
    program = IntcodeComputer(instructions, lambda: None)
    x, y = 0, 0
    grid = [["?" for _ in range(50)] for _ in range(50)]
    while not program.done:
        o = program.run()
        if o == None:
            break
        if chr(o) in "^><v":
            start = (x, y)
        if o == 10:
            x += 1
            y = 0
        else:
            grid[x][y] = chr(o)
            y += 1
    new_grid = [[p for p in row if p != "?"] for row in grid]
    new_grid = [row for row in new_grid if row]
    return grid


def solve_part_1(instructions):
    grid = run_program(instructions)
    intersections = set()
    for i in range(1, len(grid) - 1):
        for j in range(1, len(grid[0]) - 1):
            if grid[i][j] + grid[i + 1][j] + grid[i - 1][j] + grid[i][j + 1] + grid[i][j - 1] == "#" * 5:
                intersections.add((i, j))
    return sum([x * y for x, y in intersections])


def to_ascii(s):
    return [(ord(c)) for c in s] + [10]

def solve_part_2(instructions):
    main_routine = to_ascii("C,B,C,B,A,B,A,C,B,A")
    A = to_ascii("R,4,L,12,R,6,L,12")
    B = to_ascii("R,10,R,6,R,4")
    C = to_ascii("R,4,R,10,R,8,R,4")
    out = [ord('n'), 10]
    def get_input():
        if len(main_routine) > 0:
            return main_routine.pop(0)
        elif len(A) > 0:
            return A.pop(0)
        elif len(B) > 0:
            return B.pop(0)
        elif len(C) > 0:
            return C.pop(0)
        return out.pop(0)
    program = IntcodeComputer(instructions, get_input)
    program.set_val(0, 2)
    while not program.done:
        o = program.run()
    return o


def main():
    with open('input.txt') as f:
        data = list(map(int, f.read().strip().split(",")))
    sol1 = solve_part_1(data)
    print('Part 1: {}'.format(sol1))
    sol2 = solve_part_2(data)
    print('Part 2: {}'.format(sol2))


if __name__ == "__main__":
    main()
