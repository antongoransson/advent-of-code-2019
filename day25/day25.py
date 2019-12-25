import os
os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from intcode.IntcodeComputer import IntcodeComputer


def to_ascii(p_input):
    return [ord(c) for c in "\n".join(p_input)] + [ord("\n")]


def solve_part_1(instructions):
    p_input = []
    p_input = ["east",
               "east",
               "take fixed point",
               "north",
               "take spool of cat6",
               "west",
               "take shell",
               "east",
               "south",
               "west",
               "south",
               "west",
               "north",
               "take candy cane",
               "south",
               "east",
               "north",
               "west",
               "north",
               "north",
               "east",
               "south"
               ]
    p_input = to_ascii(p_input)
    def get_input():
        if not p_input:
            i = input()
            p_input.extend(list(i))
            p_input.append("\n")
        print(chr(p_input[0]), end ='')
        return p_input.pop(0)

    program = IntcodeComputer(instructions, get_input)
    while not program.done:
        o = program.run()
        if o is None:
            break
        print(chr(o), end='')


def main():
    with open('input.txt') as f:
        data = list(map(int, f.read().strip().split(",")))
    solve_part_1(data)


if __name__ == "__main__":
    main()
